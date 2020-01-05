#include <Python.h>
#include <ctype.h>
#include <datetime.h>

#define STRINGIZE(x)            #x
#define EXPAND_AND_STRINGIZE(x) STRINGIZE(x)

#define PY_VERSION_AT_LEAST_32 \
    ((PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION >= 2) || PY_MAJOR_VERSION > 3)
#define PY_VERSION_AT_LEAST_33 \
    ((PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION >= 3) || PY_MAJOR_VERSION > 3)
#define PY_VERSION_AT_LEAST_36 \
    ((PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION >= 6) || PY_MAJOR_VERSION > 3)
#define PY_VERSION_AT_LEAST_37 \
    ((PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION >= 7) || PY_MAJOR_VERSION > 3)

#if !PY_VERSION_AT_LEAST_37
static PyObject *fixed_offset;
#endif

static PyObject *utc;

#define PARSE_INTEGER(field, length, field_name)                       \
    for (i = 0; i < length; i++) {                                     \
        if (*c >= '0' && *c <= '9') {                                  \
            field = 10 * field + *c++ - '0';                           \
        }                                                              \
        else {                                                         \
            return format_unexpected_character_exception(              \
                field_name, c, (c - str) / sizeof(char), length - i);  \
        }                                                              \
    }

#define PARSE_FRACTIONAL_SECOND()                              \
    for (i = 0; i < 6; i++) {                                  \
        if (*c >= '0' && *c <= '9') {                          \
            usecond = 10 * usecond + *c++ - '0';               \
        }                                                      \
        else if (i == 0) {                                     \
            /* We need at least one digit. */                  \
            /* Trailing '.' or ',' is not allowed */           \
            return format_unexpected_character_exception(      \
                "subsecond", c, (c - str) / sizeof(char), 1);  \
        }                                                      \
        else                                                   \
            break;                                             \
    }                                                          \
                                                               \
    /* Omit excessive digits */                                \
    while (*c >= '0' && *c <= '9') c++;                        \
                                                               \
    /* If we break early, fully expand the usecond */          \
    while (i++ < 6) usecond *= 10;

#if PY_VERSION_AT_LEAST_33
    #define PARSE_SEPARATOR(separator, field_name)                                \
        if (separator) {                                                          \
            c++;                                                                  \
        }                                                                         \
        else {                                                                    \
            PyObject *unicode_str = PyUnicode_FromString(c);                      \
            PyObject *unicode_char = PyUnicode_Substring(unicode_str, 0, 1);      \
            PyErr_Format(PyExc_ValueError,                                        \
                        "Invalid character while parsing %s ('%U', Index: %lu)",  \
                        field_name, unicode_char, (c - str) / sizeof(char));      \
            Py_DECREF(unicode_str);                                               \
            Py_DECREF(unicode_char);                                              \
            return NULL;                                                          \
        }
#else
    #define PARSE_SEPARATOR(separator, field_name)                                \
        if (separator) {                                                          \
            c++;                                                                  \
        }                                                                         \
        else {                                                                    \
            if (isascii((int) *c)) {                                              \
                PyErr_Format(PyExc_ValueError,                                    \
                        "Invalid character while parsing %s ('%c', Index: %lu)",  \
                        field_name, *c, (c - str) / sizeof(char));                \
            }                                                                     \
            else {                                                                \
                PyErr_Format(PyExc_ValueError,                                    \
                        "Invalid character while parsing %s (Index: %lu)",        \
                        field_name, (c - str) / sizeof(char));                    \
            }                                                                     \
            return NULL;                                                          \
        }
#endif

static void *
format_unexpected_character_exception(char *field_name, char *c, size_t index,
                                      int expected_character_count)
{
    if (*c == '\0') {
        PyErr_Format(
            PyExc_ValueError,
            "Unexpected end of string while parsing %s. Expected %d more "
            "character%s",
            field_name, expected_character_count,
            (expected_character_count != 1) ? "s" : "");
    }
    else {
        #if PY_VERSION_AT_LEAST_33
            PyObject *unicode_str = PyUnicode_FromString(c);
            PyObject *unicode_char = PyUnicode_Substring(unicode_str, 0, 1);
            PyErr_Format(PyExc_ValueError,
                        "Invalid character while parsing %s ('%U', Index: %zu)",
                        field_name, unicode_char, index);
            Py_DECREF(unicode_str);
            Py_DECREF(unicode_char);
        #else
            if (isascii((int) *c)) {
                PyErr_Format(PyExc_ValueError,
                        "Invalid character while parsing %s ('%c', Index: %zu)",
                        field_name, *c, index);
            }
            else {
                PyErr_Format(PyExc_ValueError,
                        "Invalid character while parsing %s (Index: %zu)",
                        field_name, index);
            }
        #endif
    }
    return NULL;
}

#define IS_CALENDAR_DATE_SEPARATOR (*c == '-')
#define IS_DATE_AND_TIME_SEPARATOR (*c == 'T' || *c == ' ' || *c == 't')
#define IS_TIME_SEPARATOR (*c == ':')
#define IS_TIME_ZONE_SEPARATOR \
    (*c == 'Z' || *c == '-' || *c == '+' || *c == 'z')
#define IS_FRACTIONAL_SEPARATOR (*c == '.' || (*c == ',' && !rfc3339_only))

static PyObject *
_parse(PyObject *self, PyObject *args, int parse_any_tzinfo, int rfc3339_only)
{
    PyObject *obj;
    PyObject *tzinfo = Py_None;

    int i;
    char *str = NULL;
    char *c;
    int year = 0, month = 0, day = 0, hour = 0, minute = 0, second = 0,
        usecond = 0;
    int time_is_midnight = 0;
    int tzhour = 0, tzminute = 0, tzsign = 0;
    PyObject *delta;
    PyObject *temp;
    int extended_date_format = 0;

    if (!PyArg_ParseTuple(args, "s", &str))
        return NULL;
    c = str;

    /* Year */
    PARSE_INTEGER(year, 4, "year")

#if !PY_VERSION_AT_LEAST_36
    /* Python 3.6+ does this validation as part of datetime's C API
     * constructor. See
     * https://github.com/python/cpython/commit/b67f0967386a9c9041166d2bbe0a421bd81e10bc
     * We skip ` || year < datetime.MAXYEAR)`, since ciso8601 currently doesn't
     * support 5 character years, so it is impossible.
     */
    if (year <
        1) /* datetime.MINYEAR = 1, which is not exposed to the C API. */
    {
        PyErr_Format(PyExc_ValueError, "year %d is out of range", year);
        return NULL;
    }
#endif

    if (IS_CALENDAR_DATE_SEPARATOR) { /* Separated Month and Day (ie. MM-DD) */
        c++;
        extended_date_format = 1;

        /* Month */
        PARSE_INTEGER(month, 2, "month")

        if (*c != '\0' && !IS_DATE_AND_TIME_SEPARATOR) { /* Optional Day */
            PARSE_SEPARATOR(IS_CALENDAR_DATE_SEPARATOR, "date separator ('-')")

            /* Day */
            PARSE_INTEGER(day, 2, "day")
        }
        else if (rfc3339_only) {
            PyErr_SetString(PyExc_ValueError,
                            "Datetime string not in RFC 3339 format.");
            return NULL;
        }
        else {
            day = 1;
        }
    }
    else if (rfc3339_only) {
        PyErr_SetString(PyExc_ValueError,
                        "Datetime string not in RFC 3339 format.");
        return NULL;
    }
    else { /* Non-separated Month and Day (ie. MMDD) */
        /* Month */
        PARSE_INTEGER(month, 2, "month")
        /* Note that YYMM is not a valid timestamp. If the calendar date is not
         * separated, a day is required (ie. YYMMDD)
         */
        PARSE_INTEGER(day, 2, "day")
    }

#if !PY_VERSION_AT_LEAST_36
    /* Validation of date fields
     * These checks are needed for Python <3.6 support. See
     * https://github.com/closeio/ciso8601/pull/30 Python 3.6+ does this
     * validation as part of datetime's C API constructor. See
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
        PARSE_SEPARATOR(IS_DATE_AND_TIME_SEPARATOR,
                        "date and time separator (ie. 'T' or ' ')")

        /* Hour */
        PARSE_INTEGER(hour, 2, "hour")

        if (*c != '\0' &&
            !IS_TIME_ZONE_SEPARATOR) { /* Optional minute and second */

            if (IS_TIME_SEPARATOR) { /* Separated Minute and Second (ie. mm:ss)
                                      */
                c++;

                /* Minute */
                PARSE_INTEGER(minute, 2, "minute")

                if (*c != '\0' &&
                    !IS_TIME_ZONE_SEPARATOR) { /* Optional Second */
                    PARSE_SEPARATOR(IS_TIME_SEPARATOR, "time separator (':')")

                    /* Second */
                    PARSE_INTEGER(second, 2, "second")

                    /* Optional Fractional Second */
                    if (IS_FRACTIONAL_SEPARATOR) {
                        c++;
                        PARSE_FRACTIONAL_SECOND()
                    }
                }
                else if (rfc3339_only) {
                    PyErr_SetString(PyExc_ValueError,
                                    "RFC 3339 requires the second to be "
                                    "specified.");
                    return NULL;
                }

                if (!extended_date_format) {
                    PyErr_SetString(
                        PyExc_ValueError,
                        "Cannot combine \"basic\" date format with"
                        " \"extended\" time format (Should be either "
                        "`YYYY-MM-DDThh:mm:ss` or `YYYYMMDDThhmmss`).");
                    return NULL;
                }
            }
            else if (rfc3339_only) {
                PyErr_SetString(PyExc_ValueError,
                                "Colons separating time components are "
                                "mandatory in RFC 3339.");
                return NULL;
            }
            else { /* Non-separated Minute and Second (ie. mmss) */
                /* Minute */
                PARSE_INTEGER(minute, 2, "minute")
                if (*c != '\0' &&
                    !IS_TIME_ZONE_SEPARATOR) { /* Optional Second */
                    /* Second */
                    PARSE_INTEGER(second, 2, "second")

                    /* Optional Fractional Second */
                    if (IS_FRACTIONAL_SEPARATOR) {
                        c++;
                        PARSE_FRACTIONAL_SECOND()
                    }
                }

                if (extended_date_format) {
                    PyErr_SetString(
                        PyExc_ValueError,
                        "Cannot combine \"extended\" date format with"
                        " \"basic\" time format (Should be either "
                        "`YYYY-MM-DDThh:mm:ss` or `YYYYMMDDThhmmss`).");
                    return NULL;
                }
            }
        }
        else if (rfc3339_only) {
            PyErr_SetString(PyExc_ValueError,
                            "Minute and second are mandatory in RFC 3339");
            return NULL;
        }

        if (hour == 24 && minute == 0 && second == 0 && usecond == 0) {
            /* Special case of 24:00:00, that is allowed in ISO 8601. It is
             * equivalent to 00:00:00 the following day
             */
            if (rfc3339_only) {
                PyErr_SetString(PyExc_ValueError,
                                "An hour value of 24, while sometimes legal "
                                "in ISO 8601, is explicitly forbidden by RFC "
                                "3339.");
                return NULL;
            }
            hour = 0, minute = 0, second = 0, usecond = 0;
            time_is_midnight = 1;
        }

#if !PY_VERSION_AT_LEAST_36
        /* Validate hour/minute/second
         * Only needed for Python <3.6 support.
         * Python 3.6+ does this validation as part of datetime's constructor).
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
            if (*c == '+') {
                tzsign = 1;
            }
            else if (*c == '-') {
                tzsign = -1;
            }
            c++;

            if (tzsign != 0) {
                /* tz hour */
                PARSE_INTEGER(tzhour, 2, "tz hour")

                if (IS_TIME_SEPARATOR) { /* Optional separator */
                    c++;
                    /* tz minute */
                    PARSE_INTEGER(tzminute, 2, "tz minute")
                }
                else if (rfc3339_only) {
                    PyErr_SetString(PyExc_ValueError,
                                    "Separator between hour and minute in UTC "
                                    "offset is mandatory in RFC 3339");
                    return NULL;
                }
                else if (*c != '\0') { /* Optional tz minute */
                    PARSE_INTEGER(tzminute, 2, "tz minute")
                }
            }

            /* It's not entirely clear whether this validation check is
             * necessary under ISO 8601. For now, we will err on the side of
             * caution and prevent suspected invalid timestamps. If we need to
             * loosen this restriction later, we can.
             */
            if (tzminute > 59) {
                PyErr_SetString(PyExc_ValueError, "tzminute must be in 0..59");
                return NULL;
            }

            if (parse_any_tzinfo) {
                tzminute += 60 * tzhour;
                tzminute *= tzsign;

#if !PY_VERSION_AT_LEAST_32
                if (fixed_offset == NULL || utc == NULL) {
                    PyErr_SetString(PyExc_ImportError,
                                    "Cannot parse a timestamp with time zone "
                                    "information without the pytz dependency. "
                                    "Install it with `pip install pytz`.");
                    return NULL;
                }
#endif

                if (tzminute == 0) {
                    tzinfo = utc;
                }
                else {
#if PY_VERSION_AT_LEAST_37
                    delta = PyDelta_FromDSU(0, 60 * tzminute, 0);
                    tzinfo = PyTimeZone_FromOffset(delta);
                    Py_DECREF(delta);
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
        else if (rfc3339_only) {
            PyErr_SetString(PyExc_ValueError,
                            "UTC offset is mandatory in RFC 3339 format.");
            return NULL;
        }
    }
    else if (rfc3339_only) {
        PyErr_SetString(PyExc_ValueError,
                        "Time is mandatory in RFC 3339 format.");
        return NULL;
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

    if (obj && time_is_midnight) {
        delta = PyDelta_FromDSU(1, 0, 0); /* 1 day */
        temp = obj;
        obj = PyNumber_Add(temp, delta);
        Py_DECREF(delta);
        Py_DECREF(temp);
    }

    return obj;
}

static PyObject *
parse_datetime_as_naive(PyObject *self, PyObject *args)
{
    return _parse(self, args, 0, 0);
}

static PyObject *
parse_datetime(PyObject *self, PyObject *args)
{
    return _parse(self, args, 1, 0);
}

static PyObject *
parse_rfc3339(PyObject *self, PyObject *args)
{
    return _parse(self, args, 1, 1);
}

static PyMethodDef CISO8601Methods[] = {
    {"parse_datetime", parse_datetime, METH_VARARGS,
     "Parse a ISO8601 date time string."},
    {"parse_datetime_as_naive", parse_datetime_as_naive, METH_VARARGS,
     "Parse a ISO8601 date time string, ignoring the time zone component."},
    {"parse_rfc3339", parse_rfc3339, METH_VARARGS,
     "Parse an RFC 3339 date time string."},
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
#if !PY_VERSION_AT_LEAST_32
    PyObject *pytz;
#elif !PY_VERSION_AT_LEAST_37
    PyObject *datetime;
#endif

#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    PyObject *module = Py_InitModule("ciso8601", CISO8601Methods);
#endif
    /* CISO8601_VERSION is defined in setup.py */
    PyModule_AddStringConstant(module, "__version__",
                               EXPAND_AND_STRINGIZE(CISO8601_VERSION));

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
