#include <Python.h>
#include <datetime.h>

static PyObject* pytz_fixed_offset;
static PyObject* pytz_utc;

static void* format_unexpected_character_exception(char* field_name, char c, int index, int expected_character_count){
    if (c == '\0')
        PyErr_Format(PyExc_ValueError, "Unexpected end of string while parsing %s. Expected %d more character%s", field_name, expected_character_count, (expected_character_count != 1) ? "s": "");
    else
        PyErr_Format(PyExc_ValueError, "Invalid character while parsing %s ('%c', Index: %d)", field_name, c, index);
    return NULL;
}

static int parse_integer(char** c, char* str, int length, char* field_name){
    int i = 0;
    int result = 0;

    for (i = 0; i < length; i++) {
        if (**c >= '0' && **c <= '9'){
            result = 10 * result + **c - '0';
            (*c)++;
        } else {
            return format_unexpected_character_exception(field_name, **c, (*c-str)/sizeof(char), length - i);
        }
    }
    return result;
}

static int parse_date_separator(char** c, char* str){
    if (**c == '-'){ // Optional separator
        (*c)++;
        return 1;
    } else {
        format_unexpected_character_exception("date separator ('-')", **c, (*c-str)/sizeof(char), 1);
        return 0;
    }
}

static int parse_time_separator(char** c, char* str){ //TODO: Merge with parse_date_separator?
    if (**c == ':'){ // Optional separator
        (*c)++;
        return 1;
    }
    else {
        format_unexpected_character_exception("time separator (':')", **c, (*c-str)/sizeof(char), 1);
        return 0;
    }
}

static int is_date_and_time_separator(char c){
    return c == 'T' || c == ' ';
}

static void parse_month_day(char** c, char* str, int* month, int* day){
    if (**c == '-'){
        (*c)++;\
        *month = parse_integer(c, str, 2, "month");
        if (PyErr_Occurred())
            return NULL;

        if (**c != '\0' && !is_date_and_time_separator(**c)){ // Optional day
            parse_date_separator(c, str);
            if (PyErr_Occurred())
                return NULL;

            *day = parse_integer(c, str, 2, "day");
            if (PyErr_Occurred())
                return NULL;
        } else {
            *day = 1;
        }

    } else {
        //Note: Day is mandatory if there were no separators
        *month = parse_integer(c, str, 2, "month");
        if (PyErr_Occurred())
            return NULL;

        *day = parse_integer(c, str, 2, "day");
        if (PyErr_Occurred())
            return NULL;
    }
}

static void parse_date_and_time_delimiter(char** c, char* str){
    if (is_date_and_time_separator(**c)){
        (*c)++;
    } else {
        format_unexpected_character_exception("date and time separator (ie. 'T' or ' ')", **c, (*c-str)/sizeof(char), 1);
    }
}

static void parse_subsecond(char** c, char* str, int* usecond){
    int i = 0;
    (*c)++;
    for (i = 0; i < 6; i++) {
        if (**c >= '0' && **c <= '9'){
            *usecond = 10 * *usecond + **c - '0';
            (*c)++;
        } else if (i == 0){
            //We need at least one digit. Trailing '.'s are not allowed
            return format_unexpected_character_exception("subsecond", **c, (*c-str)/sizeof(char), 1);
        } else
            break;
    }

    // Omit excessive digits
    // TODO: Should this do rounding instead?
    while (**c >= '0' && **c <= '9')
        (*c)++;

    // If we break early, fully expand the usecond
    while (i++ < 6)
        *usecond *= 10;
}

static void parse_second(char** c, char* str, int* second, int* usecond){
    *second = parse_integer(c, str, 2, "second");
    if (PyErr_Occurred())
            return NULL;

    if (**c == '.' || **c == ','){
        parse_subsecond(c, str, usecond);
        if (PyErr_Occurred())
            return NULL;
    }
}

static int is_time_zone_separator(char c){
    return c == 'Z' || c == '-' || c == '+';
}

static void parse_minute_second(char** c, char* str, int* minute, int* second, int* usecond){
    if (**c == ':'){
        (*c)++;
        *minute = parse_integer(c, str, 2, "minute");
        if (PyErr_Occurred())
            return NULL;

        if (**c != '\0' && !is_time_zone_separator(**c)){ // Optional second
            parse_time_separator(c, str);
            if (PyErr_Occurred())
                return NULL;

            parse_second(c, str, second, usecond);
            if (PyErr_Occurred())
                return NULL;
        }
    } else {
        *minute = parse_integer(c, str, 2, "minute");
        if (PyErr_Occurred())
            return NULL;

        if (**c != '\0' && !is_time_zone_separator(**c)){ // Optional second
            parse_second(c, str, second, usecond);
            if (PyErr_Occurred())
                return NULL;
        }
    }
}

static void parse_tzinfo(char** c, char* str, PyObject** tzinfo){
    // Time zone designator (Z or +hh:mm or -hh:mm)
    int aware = 0;
    int tzhour = 0, tzminute = 0, tzsign = 0;
    if (**c == 'Z')
    {
        // UTC
        (*c)++;
        aware = 1;
    }
    else if (**c == '+')
    {
        (*c)++;
        aware = 1;
        tzsign = 1;
    }
    else if (**c == '-')
    {
        (*c)++;
        aware = 1;
        tzsign = -1;
    }

    if (tzsign != 0) {
        tzhour = parse_integer(c, str, 2, "tz hour");
        if (PyErr_Occurred())
            return NULL;

        if (**c == ':') { // Optional separator
            (*c)++;
            tzminute = parse_integer(c, str, 2, "tz minute");
            if (PyErr_Occurred())
                return NULL;
        } else if (**c != '\0'){ // Optional minute
            tzminute = parse_integer(c, str, 2, "tz minute");
            if (PyErr_Occurred())
                return NULL;
        }
    }

    if (aware && pytz_fixed_offset != NULL) {
        tzminute += 60 * tzhour;
        tzminute *= tzsign;

        if (tzminute == 0)
            *tzinfo = pytz_utc;
        else if (abs(tzminute) >= 1440){
            // If we don't check this here, the interpreter crashes.
            PyErr_Format(PyExc_ValueError, "Absolute tz offset is too large (%d)", tzminute);
            return NULL;
        }
        else
            *tzinfo = PyObject_CallFunction(pytz_fixed_offset, "i", tzminute);
    }
}

static void parse_timestamp(char** c, char* str, int* hour, int* minute, int* second, int* usecond, PyObject** tzinfo){
    parse_date_and_time_delimiter(c, str);
    if (PyErr_Occurred())
        return NULL;

    *hour = parse_integer(c, str, 2, "hour");
    if (PyErr_Occurred())
        return NULL;

    if (**c != '\0' && !is_time_zone_separator(**c)){
        parse_minute_second(c, str, minute, second, usecond);
        if (PyErr_Occurred())
            return NULL;
    }
    if (**c != '\0'){
        parse_tzinfo(c, str, tzinfo);
        if (PyErr_Occurred())
            return NULL;
    }
}

static PyObject* parse_datetime(PyObject* self, PyObject* args)
{
    PyObject *obj;
    PyObject* tzinfo = Py_None;

    char* str = NULL;
    char* c;
    int year = 0, month = 0, day = 0, hour = 0, minute = 0, second = 0, usecond = 0;
    int time_is_midnight = 0;

    if (!PyArg_ParseTuple(args, "s", &str))
        return NULL;
    c = str;

    // Year
    year = parse_integer(&c, str, 4, "year");
    if (PyErr_Occurred())
        return NULL;
    //TODO: Check range of year if necessary

    if (*c != '\0' && !is_date_and_time_separator(*c)){
        parse_month_day(&c, str, &month, &day);
        if (PyErr_Occurred())
            return NULL;
    }

    // Validation of date fields
    // These checks are needed for Python 2 support. See https://github.com/closeio/ciso8601/pull/30
    // Python 3 does this validation as part of Datetime's C API constructor.
    // If ciso8601 were to drop Python 2 support, these might still be useful, since they short-circuit parsing.
    if (month < 1 || month > 12){
        PyErr_SetString(PyExc_ValueError, "month must be in 1..12");
        return NULL;
    }


    // Only needed for Python 2 support (or performance short-circuiting. Python 3 does this validation as part of Datetime's constructor).
    if (day < 1) {
        PyErr_SetString(PyExc_ValueError, "day is out of range for month");
        return NULL;
    }

    // Validate max day based on month
    // Only needed for Python 2 support (or performance short-circuiting. Python 3 does this validation as part of Datetime's constructor).
    switch (month) {
        case 2:
            // In the Gregorian calendar three criteria must be taken into account to identify leap years:
            // * The year can be evenly divided by 4;
            // * If the year can be evenly divided by 100, it is NOT a leap year, unless;
            // * The year is also evenly divisible by 400. Then it is a leap year.
            if (day > 28) {
                unsigned int leap = (year % 4 == 0) && (year % 100 || (year % 400 == 0));
                if (leap == 0 || day > 29) {
                    PyErr_SetString(PyExc_ValueError, "day is out of range for month");
                    return NULL;
                }
            }
            break;
        case 4: case 6: case 9: case 11:
            if (day > 30) {
                PyErr_SetString(PyExc_ValueError, "day is out of range for month");
                return NULL;
            }
            break;
        default:
            // For other months i.e. 1, 3, 5, 7, 8, 10 and 12
            if (day > 31) {
                PyErr_SetString(PyExc_ValueError, "day is out of range for month");
                return NULL;
            }
            break;
    }


    if (*c != '\0' && !is_time_zone_separator(*c)){
        parse_timestamp(&c, str, &hour, &minute, &second, &usecond, &tzinfo);
        if (PyErr_Occurred())
            return NULL;
    }

    if (hour == 24 && minute == 0 && second == 0 && usecond == 0){
        //Special case of 24:00:00, that is allowed in ISO 8601. It is equivalent to 00:00:00 the following day
        hour = 0, minute = 0, second = 0, usecond = 0;
        time_is_midnight = 1;
    }

    // Validate hour/minute/second
    // Only needed for Python 2 support (or performance short-circuiting. Python 3 does this validation as part of Datetime's constructor).
    if (hour > 23){
        PyErr_SetString(PyExc_ValueError, "hour must be in 0..23");
        return NULL;
    }
    if (minute > 59){
        PyErr_SetString(PyExc_ValueError, "minute must be in 0..59");
        return NULL;
    }
    if (second > 59){
        PyErr_SetString(PyExc_ValueError, "second must be in 0..59");
        return NULL;
    }

    
    // Make sure that there is no more to parse.
    if (*c != '\0'){
        PyErr_Format(PyExc_ValueError, "unconverted data remains: '%s'", c);
        return NULL;
    }

    obj = PyDateTimeAPI->DateTime_FromDateAndTime(
        year,
        month,
        day,
        hour,
        minute,
        second,
        usecond,
        tzinfo,
        PyDateTimeAPI->DateTimeType
    );
    

    if (tzinfo != Py_None && tzinfo != pytz_utc)
        Py_DECREF(tzinfo);

    if (PyErr_Occurred())
        return NULL;

    if (time_is_midnight){
        obj = PyNumber_Add(obj, PyDelta_FromDSU(1,0,0)); // 1 day
        if (PyErr_Occurred())
            return NULL;
    }
    

    if (!obj) { //TODO: Can this ever actually be true?
        PyErr_SetString(PyExc_ValueError, "Unable to create datetime object");
        return NULL;
    }

    return obj;
}

static PyMethodDef CISO8601Methods[] =
{
     {"parse_datetime", parse_datetime, METH_VARARGS, "Parse a ISO8601 date time string."},
     {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "ciso8601",
    NULL,
    -1,
    CISO8601Methods,
    NULL,
    NULL,
    NULL,
    NULL,
};
#endif

PyMODINIT_FUNC
#if PY_MAJOR_VERSION >= 3
PyInit_ciso8601(void)
#else
initciso8601(void)
#endif
{
    PyObject* pytz;
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    (void) Py_InitModule("ciso8601", CISO8601Methods);
#endif
    PyDateTime_IMPORT;
    pytz = PyImport_ImportModule("pytz");
    if (pytz == NULL)
    {
        PyErr_Clear();
    }
    else
    {
        pytz_fixed_offset = PyObject_GetAttrString(pytz, "FixedOffset");
        pytz_utc = PyObject_GetAttrString(pytz, "UTC");
    }
#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
