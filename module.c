#include <Python.h>
#include <datetime.h>

static PyObject* pytz_fixed_offset;
static PyObject* pytz_utc;

static PyObject* _parse(PyObject* self, PyObject* args, int parse_tzinfo)
{
    PyObject *obj;
    char* str = NULL;
    char* c;
    int year = 0, month = 0, day = 0, hour = 0, minute = 0, second = 0, usecond = 0, i = 0;
    int aware = 0; // 1 if aware
    int tzhour = 0, tzminute = 0, tzsign = 0;
 
    if (!PyArg_ParseTuple(args, "s", &str))
        return NULL;
    c = str;

    // Year
    for (i = 0; i < 4; i++) {
        if (*c >= '0' && *c <= '9')
            year = 10 * year + *c++ - '0';
        else
            Py_RETURN_NONE;
    }

    if (*c == '-') // Optional separator
        c++;

    // Month
    for (i = 0; i < 2; i++) {
        if (*c >= '0' && *c <= '9')
            month = 10 * month + *c++ - '0';
        else
            Py_RETURN_NONE;
    }

    if (*c == '-') // Optional separator
        c++;

    // Day
    for (i = 0; i < 2; i++) {
        if (*c >= '0' && *c <= '9')
            day = 10 * day + *c++ - '0';
        else
            break;
    }

    if (day == 0) day = 1; // YYYY-MM format

    if (*c == 'T' || *c == ' ') // Time separator
    {
        c++;

        // Hour
        for (i = 0; i < 2; i++) {
            if (*c >= '0' && *c <= '9')
                hour = 10 * hour + *c++ - '0';
            else
                Py_RETURN_NONE;
        }

        if (*c == ':') // Optional separator
            c++;

        // Minute (optional)
        for (i = 0; i < 2; i++) {
            if (*c >= '0' && *c <= '9')
                minute = 10 * minute + *c++ - '0';
            else
                break;
        }

        if (*c == ':') // Optional separator
            c++;

        // Second (optional)
        for (i = 0; i < 2; i++) {
            if (*c >= '0' && *c <= '9')
                second = 10 * second + *c++ - '0';
            else
                break;
        }

        if (*c == '.' || *c == ',') // separator
        {
            c++;

            // Parse fraction of second up to 6 places
            for (i = 0; i < 6; i++) {
                if (*c >= '0' && *c <= '9')
                    usecond = 10 * usecond + *c++ - '0';
                else
                    break;
            }

            // Omit excessive digits
            while (*c >= '0' && *c <= '9')
                c++;

            // If we break early, fully expand the usecond
            while (i++ < 6)
                usecond *= 10;

        }
    }

    if (parse_tzinfo)
    {
        // Time zone designator (Z or +hh:mm or -hh:mm)
        if (*c == 'Z')
        {
            // UTC
            c++;
            aware = 1;
        }
        else if (*c == '+')
        {
            c++;
            aware = 1;
            tzsign = 1;
        }
        else if (*c == '-')
        {
            c++;
            aware = 1;
            tzsign = -1;
        }

        if (tzsign != 0) {
            for (i = 0; i < 2; i++) {
                if (*c >= '0' && *c <= '9')
                    tzhour = 10 * tzhour + *c++ - '0';
                else
                    break;
            }

            if (*c == ':') // Optional separator
                c++;

            for (i = 0; i < 2; i++) {
                if (*c >= '0' && *c <= '9')
                    tzminute = 10 * tzminute + *c++ - '0';
                else
                    break;
            }
        }
    }


    obj = PyDateTime_FromDateAndTime(year, month, day, hour, minute, second, usecond);
    if (!obj)
        Py_RETURN_NONE;

    if (aware && pytz_fixed_offset != NULL) {

        PyObject* replace;
        PyObject* aware_obj;
        PyObject* args;
        PyObject* kwargs;
        PyObject* tzinfo = NULL;

        tzminute += 60*tzhour;
        tzminute *= tzsign;

        if (tzminute == 0)
            tzinfo = pytz_utc;
        if (!tzinfo)
            tzinfo = PyObject_CallFunction(pytz_fixed_offset, "i", tzminute);
        if (!tzinfo)
            return obj;

        // Assume these will succeed
        args = PyTuple_New(0);
        replace = PyObject_GetAttrString(obj, "replace");
        kwargs = PyDict_New();
        PyDict_SetItemString(kwargs, "tzinfo", tzinfo);
        aware_obj = PyObject_Call(replace, args, kwargs);

        Py_DECREF(obj);
        Py_DECREF(replace);
        Py_DECREF(kwargs);
        Py_DECREF(args);
        if (tzinfo != pytz_utc)
            Py_DECREF(tzinfo);

        obj = aware_obj;

    }

    return obj;
}

static PyObject* parse_datetime_unaware(PyObject* self, PyObject* args)
{
    return _parse(self, args, 0);
}
 
static PyObject* parse_datetime(PyObject* self, PyObject* args)
{
    return _parse(self, args, 1);
}
 
static PyMethodDef CISO8601Methods[] =
{
     {"parse_datetime", parse_datetime, METH_VARARGS, "Parse a ISO8601 date time string."},
     {"parse_datetime_unaware", parse_datetime_unaware, METH_VARARGS, "Parse a ISO8601 date time string, ignoring the time zone component."},
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
        pytz_fixed_offset = PyObject_GetAttrString(pytz, "_FixedOffset");
        pytz_utc = PyObject_GetAttrString(pytz, "UTC");
    }
#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
