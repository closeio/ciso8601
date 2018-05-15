#include <Python.h>
#include <datetime.h>

static PyObject *fixed_offset;
static PyObject *utc;

#define PY_VERSION_AT_LEAST_32 \
    ((PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION >= 2) || PY_MAJOR_VERSION > 3)
#define PY_VERSION_AT_LEAST_36 \
    ((PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION >= 6) || PY_MAJOR_VERSION > 3)
#define PY_VERSION_AT_LEAST_37 \
    ((PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION >= 7) || PY_MAJOR_VERSION > 3)

static void *
format_unexpected_character_exception(char *field_name, char c, int index,
                                      int expected_character_count)
{
    if (c == '\0')
        PyErr_Format(
            PyExc_ValueError,
            "Unexpected end of string while parsing %s. Expected %d more "
            "character%s",
            field_name, expected_character_count,
            (expected_character_count != 1) ? "s" : "");
    else
        PyErr_Format(PyExc_ValueError,
                     "Invalid character while parsing %s ('%c', Index: %d)",
                     field_name, c, index);
    return NULL;
}

#define IS_DATE_AND_TIME_SEPARATOR (*c == 'T' || *c == ' ')
#define IS_TIME_ZONE_SEPARATOR (*c == 'Z' || *c == '-' || *c == '+')
#define IS_FRACTIONAL_SEPARATOR (*c == '.' || *c == ',')

static PyObject *
_parse(PyObject *self, PyObject *args, int parse_any_tzinfo)
{
    PyObject *obj;
    PyObject *tzinfo = Py_None;

    int i;
    char *str = NULL;
    char *c;
    int year = 0, month = 0, day = 0, hour = 0, minute = 0, second = 0,
        usecond = 0;
    int time_is_midnight = 0;
    int aware = 0;
    int tzhour = 0, tzminute = 0, tzsign = 0;

    if (!PyArg_ParseTuple(args, "s", &str))
        return NULL;
    c = str;

    /* Year */
    for (i = 0; i < 4; i++) {
        if (*c >= '0' && *c <= '9') {
            year = 10 * year + *c++ - '0';
        }
        else {
            return format_unexpected_character_exception(
                "year", *c, (c - str) / sizeof(char), 4 - i);
        }
    }

#if !PY_VERSION_AT_LEAST_36
    /* Python 3.6+ does this validation as part of Datetime's C API
     * constructor. See
     * https://github.com/python/cpython/commit/b67f0967386a9c9041166d2bbe0a421bd81e10bc
     * We skip ` || year < datetime.MAXYEAR)`, since cio8601 currently doesn't
     * support 5 character years, so it is impossible.
     */
    if (year <
        1) /* datetime.MINYEAR = 1, which is not exposed to the C API. */
    {
        PyErr_Format(PyExc_ValueError, "year %d is out of range", year);
        return NULL;
    }
#endif

    if (*c == '-') { /* Separated Month and Day (ie. MM-DD) */
        c++;
        /* Month */
        for (i = 0; i < 2; i++) {
            if (*c >= '0' && *c <= '9') {
                month = 10 * month + *c++ - '0';
            }
            else {
                return format_unexpected_character_exception(
                    "month", *c, (c - str) / sizeof(char), 2 - i);
            }
        }
        if (*c != '\0' && !IS_DATE_AND_TIME_SEPARATOR) { /* Optional Day */
            if (*c == '-') {
                c++;
            }
            else {
                PyErr_Format(
                    PyExc_ValueError,
                    "Invalid character while parsing date separator ('-') "
                    "('%c', Index: %d)",
                    *c, (c - str) / sizeof(char));
                return NULL;
            }
            /* Day */
            for (i = 0; i < 2; i++) {
                if (*c >= '0' && *c <= '9') {
                    day = 10 * day + *c++ - '0';
                }
                else {
                    return format_unexpected_character_exception(
                        "day", *c, (c - str) / sizeof(char), 2 - i);
                }
            }
        }
        else {
            day = 1;
        }
    }
    else { /* Non-separated Month and Day (ie. MMDD) */
        /* Month */
        for (i = 0; i < 2; i++) {
            if (*c >= '0' && *c <= '9') {
                month = 10 * month + *c++ - '0';
            }
            else {
                return format_unexpected_character_exception(
                    "month", *c, (c - str) / sizeof(char), 2 - i);
            }
        }
        /* Note that YYMM is not a valid timestamp. If the calendar date is not
         * separated, a day is required (ie. YYMMDD)
         */
        for (i = 0; i < 2; i++) {
            if (*c >= '0' && *c <= '9') {
                day = 10 * day + *c++ - '0';
            }
            else {
                return format_unexpected_character_exception(
                    "day", *c, (c - str) / sizeof(char), 2 - i);
            }
        }
    }

#if !PY_VERSION_AT_LEAST_36
    /* Validation of date fields
     * These checks are needed for Python <3.6 support. See
     * https://github.com/closeio/ciso8601/pull/30 Python 3.6+ does this
     * validation as part of Datetime's C API constructor. See
     * https://github.com/python/cpython/commit/b67f0967386a9c9041166d2bbe0a421bd81e10bc
     */
    if (month < 1 || month > 12) {
        PyErr_SetString(PyExc_ValueError, "month must be in 1..12");
        return NULL;
    }

    if (day < 1) {
        PyErr_SetString(PyExc_ValueError, "day is out of range for month");
        return NULL;
    }

    /* Validate max day based on month */
    switch (month) {
        case 2:
            /* In the Gregorian calendar three criteria must be taken into
             * account to identify leap years:
             *     -The year can be evenly divided by 4;
             *     -If the year can be evenly divided by 100, it is NOT a leap
             * year, unless;
             *     -The year is also evenly divisible by 400. Then it is a leap
             * year.
             */
            if (day > 28) {
                unsigned int leap =
                    (year % 4 == 0) && (year % 100 || (year % 400 == 0));
                if (leap == 0 || day > 29) {
                    PyErr_SetString(PyExc_ValueError,
                                    "day is out of range for month");
                    return NULL;
                }
            }
            break;
        case 4:
        case 6:
        case 9:
        case 11:
            if (day > 30) {
                PyErr_SetString(PyExc_ValueError,
                                "day is out of range for month");
                return NULL;
            }
            break;
        default:
            /* For other months i.e. 1, 3, 5, 7, 8, 10 and 12 */
            if (day > 31) {
                PyErr_SetString(PyExc_ValueError,
                                "day is out of range for month");
                return NULL;
            }
            break;
    }
#endif

    if (*c != '\0') {
        /* Date and time separator */
        if (IS_DATE_AND_TIME_SEPARATOR) {
            c++;
        }
        else {
            PyErr_Format(
                PyExc_ValueError,
                "Invalid character while parsing date and time separator "
                "(ie. 'T' or ' ') ('%c', Index: %d)",
                *c, (c - str) / sizeof(char));
            return NULL;
        }

        /* Hour */
        for (i = 0; i < 2; i++) {
            if (*c >= '0' && *c <= '9') {
                hour = 10 * hour + *c++ - '0';
            }
            else {
                return format_unexpected_character_exception(
                    "hour", *c, (c - str) / sizeof(char), 2 - i);
            }
        }
        if (*c != '\0' &&
            !IS_TIME_ZONE_SEPARATOR) { /* Optional minute and second */

            if (*c == ':') { /* Separated Minute and Second (ie. mm:ss) */
                c++;
                /* Minute */
                for (i = 0; i < 2; i++) {
                    if (*c >= '0' && *c <= '9') {
                        minute = 10 * minute + *c++ - '0';
                    }
                    else {
                        return format_unexpected_character_exception(
                            "minute", *c, (c - str) / sizeof(char), 2 - i);
                    }
                }
                if (*c != '\0' &&
                    !IS_TIME_ZONE_SEPARATOR) { /* Optional Second */
                    if (*c == ':') {
                        c++;
                    }
                    else {
                        PyErr_Format(PyExc_ValueError,
                                     "Invalid character while parsing time "
                                     "separator (':') "
                                     "('%c', Index: %d)",
                                     *c, (c - str) / sizeof(char));
                        return NULL;
                    }
                    /* Second */
                    for (i = 0; i < 2; i++) {
                        if (*c >= '0' && *c <= '9') {
                            second = 10 * second + *c++ - '0';
                        }
                        else {
                            return format_unexpected_character_exception(
                                "second", *c, (c - str) / sizeof(char), 2 - i);
                        }
                    }
                    /* Optional Fractional Second */
                    if (IS_FRACTIONAL_SEPARATOR) {
                        c++;
                        for (i = 0; i < 6; i++) {
                            if (*c >= '0' && *c <= '9') {
                                usecond = 10 * usecond + *c++ - '0';
                            }
                            else if (i == 0) {
                                /* We need at least one digit. Trailing '.' or
                                 * ',' is not allowed
                                 */
                                return format_unexpected_character_exception(
                                    "subsecond", *c, (c - str) / sizeof(char),
                                    1);
                            }
                            else
                                break;
                        }

                        /* Omit excessive digits */
                        /* TODO: Should this do rounding instead? */
                        while (*c >= '0' && *c <= '9') c++;

                        /* If we break early, fully expand the usecond */
                        while (i++ < 6) usecond *= 10;
                    }
                }
            }
            else { /* Non-separated Minute and Second (ie. mmss) */
                /* Minute */
                for (i = 0; i < 2; i++) {
                    if (*c >= '0' && *c <= '9') {
                        minute = 10 * minute + *c++ - '0';
                    }
                    else {
                        return format_unexpected_character_exception(
                            "minute", *c, (c - str) / sizeof(char), 2 - i);
                    }
                }
                if (*c != '\0' &&
                    !IS_TIME_ZONE_SEPARATOR) { /* Optional Second */
                    /* Second */
                    for (i = 0; i < 2; i++) {
                        if (*c >= '0' && *c <= '9') {
                            second = 10 * second + *c++ - '0';
                        }
                        else {
                            return format_unexpected_character_exception(
                                "second", *c, (c - str) / sizeof(char), 2 - i);
                        }
                    }
                    /* Optional Fractional Second */
                    if (IS_FRACTIONAL_SEPARATOR) {
                        c++;
                        for (i = 0; i < 6; i++) {
                            if (*c >= '0' && *c <= '9') {
                                usecond = 10 * usecond + *c++ - '0';
                            }
                            else if (i == 0) {
                                /* We need at least one digit. Trailing '.' or
                                 * ',' is not allowed
                                 */
                                return format_unexpected_character_exception(
                                    "subsecond", *c, (c - str) / sizeof(char),
                                    1);
                            }
                            else
                                break;
                        }

                        /* Omit excessive digits */
                        /* TODO: Should this do rounding instead? */
                        while (*c >= '0' && *c <= '9') c++;

                        /* If we break early, fully expand the usecond */
                        while (i++ < 6) usecond *= 10;
                    }
                }
            }
        }

        if (hour == 24 && minute == 0 && second == 0 && usecond == 0) {
            /* Special case of 24:00:00, that is allowed in ISO 8601. It is
             * equivalent to 00:00:00 the following day
             */
            hour = 0, minute = 0, second = 0, usecond = 0;
            time_is_midnight = 1;
        }

#if !PY_VERSION_AT_LEAST_36
        /* Validate hour/minute/second
         * Only needed for Python <3.6 support.
         * Python 3.6+ does this validation as part of Datetime's constructor).
         */
        if (hour > 23) {
            PyErr_SetString(PyExc_ValueError, "hour must be in 0..23");
            return NULL;
        }
        if (minute > 59) {
            PyErr_SetString(PyExc_ValueError, "minute must be in 0..59");
            return NULL;
        }
        if (second > 59) {
            PyErr_SetString(PyExc_ValueError, "second must be in 0..59");
            return NULL;
        }
#endif

        /* Optional tzinfo */
        if (IS_TIME_ZONE_SEPARATOR) {
            if (*c == 'Z') {
                /* UTC */
                c++;
                aware = 1;
            }
            else if (*c == '+') {
                c++;
                aware = 1;
                tzsign = 1;
            }
            else if (*c == '-') {
                c++;
                aware = 1;
                tzsign = -1;
            }
            if (tzsign != 0) {
                /* tz hour */
                for (i = 0; i < 2; i++) {
                    if (*c >= '0' && *c <= '9') {
                        tzhour = 10 * tzhour + *c++ - '0';
                    }
                    else {
                        return format_unexpected_character_exception(
                            "tz hour", *c, (c - str) / sizeof(char), 2 - i);
                    }
                }

                if (*c == ':') { /* Optional separator */
                    c++;
                    /* tz minute */
                    for (i = 0; i < 2; i++) {
                        if (*c >= '0' && *c <= '9') {
                            tzminute = 10 * tzminute + *c++ - '0';
                        }
                        else {
                            return format_unexpected_character_exception(
                                "tz minute", *c, (c - str) / sizeof(char),
                                2 - i);
                        }
                    }
                }
                else if (*c != '\0') { /* Optional tz minute */
                    for (i = 0; i < 2; i++) {
                        if (*c >= '0' && *c <= '9') {
                            tzminute = 10 * tzminute + *c++ - '0';
                        }
                        else {
                            return format_unexpected_character_exception(
                                "tz minute", *c, (c - str) / sizeof(char),
                                2 - i);
                        }
                    }
                }
            }

            /* It's not entirely clear whether this validation check is
             * necessary under ISO 8601. For now, we will error on the side of
             * caution and prevent suspected invalid timestamps If we need to
             * loosen this restriction later, we can.
             */
            if (tzminute > 59) {
                PyErr_SetString(PyExc_ValueError, "tzminute must be in 0..59");
                return NULL;
            }

            if (aware && parse_any_tzinfo) {
                tzminute += 60 * tzhour;
                tzminute *= tzsign;

#if !PY_VERSION_AT_LEAST_37
                if (fixed_offset == NULL || utc == NULL) {
                    PyErr_SetString(
                        PyExc_ImportError,
                        "Cannot parse an aware timestamp without pytz. "
                        "Install it with `pip install pytz`.");
                    return NULL;
                }
#endif

                if (tzminute == 0) {
                    tzinfo = utc;
                }
                else {
#if PY_VERSION_AT_LEAST_37
                    tzinfo = PyTimeZone_FromOffset(
                        PyDelta_FromDSU(0, 60 * tzminute, 0));
#elif PY_VERSION_AT_LEAST_32
                    tzinfo = PyObject_CallFunction(
                        fixed_offset, "N",
                        PyDelta_FromDSU(0, 60 * tzminute, 0));
#else
                    tzinfo =
                        PyObject_CallFunction(fixed_offset, "i", tzminute);
#endif
                    if (tzinfo == NULL) /* ie. PyErr_Occurred() */
                        return NULL;
                }
            }
        }
    }

    /* Make sure that there is no more to parse. */
    if (*c != '\0') {
        PyErr_Format(PyExc_ValueError, "unconverted data remains: '%s'", c);
        return NULL;
    }

    obj = PyDateTimeAPI->DateTime_FromDateAndTime(
        year, month, day, hour, minute, second, usecond, tzinfo,
        PyDateTimeAPI->DateTimeType);

    if (tzinfo != Py_None && tzinfo != utc)
        Py_DECREF(tzinfo);

    if (obj && time_is_midnight)
        obj = PyNumber_Add(obj, PyDelta_FromDSU(1, 0, 0)); /* 1 day */

    return obj;
}

static PyObject *
parse_datetime_as_naive(PyObject *self, PyObject *args)
{
    return _parse(self, args, 0);
}

PyObject *
parse_datetime(PyObject *self, PyObject *args)
{
    return _parse(self, args, 1);
}

static PyMethodDef CISO8601Methods[] = {
    {"parse_datetime", parse_datetime, METH_VARARGS,
     "Parse a ISO8601 date time string."},
    {"parse_datetime_as_naive", parse_datetime_as_naive, METH_VARARGS,
     "Parse a ISO8601 date time string, ignoring the time zone component."},
    {NULL, NULL, 0, NULL}};

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
    PyObject *pytz;
    PyObject *datetime;
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    (void)Py_InitModule("ciso8601", CISO8601Methods);
#endif
    PyDateTime_IMPORT;
#if PY_VERSION_AT_LEAST_37
    utc = PyDateTime_TimeZone_UTC;
#elif PY_VERSION_AT_LEAST_32
    datetime = PyImport_ImportModule("datetime");
    if (datetime == NULL)
        return NULL;
    fixed_offset = PyObject_GetAttrString(datetime, "timezone");
    if (fixed_offset == NULL)
        return NULL;
    utc = PyObject_GetAttrString(fixed_offset, "utc");
    if (utc == NULL)
        return NULL;
#else
    pytz = PyImport_ImportModule("pytz");
    if (pytz == NULL) {
        PyErr_Clear();
    }
    else {
        fixed_offset = PyObject_GetAttrString(pytz, "FixedOffset");
        utc = PyObject_GetAttrString(pytz, "UTC");
    }
#endif
#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
