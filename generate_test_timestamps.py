import datetime
import pytz

from collections import namedtuple


def __merge_dicts(*dict_args):
    # Only needed for Python <3.5 support. In Python 3.5+, you can use the {**a, **b} syntax.
    """
    From: https://stackoverflow.com/a/26853961
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


NumberField = namedtuple('NumberField', ['min_width', 'max_width', 'min_value', 'max_value'])
NUMBER_FIELDS = {
    "year": NumberField(4, 4, 1, 9999),
    "month": NumberField(2, 2, 1, 12),
    "day": NumberField(2, 2, 1, 31),
    "hour": NumberField(2, 2, 0, 24),  # 24 = special midnight value
    "minute": NumberField(2, 2, 0, 59),
    "second": NumberField(2, 2, 0, 60),  # 60 = Leap second
    "microsecond": NumberField(1, None, 0, None),  # Can have unbounded characters
    "tzhour": NumberField(2, 2, 0, 23),
    "tzminute": NumberField(2, 2, 0, 59)
}

PADDED_NUMBER_FIELD_FORMATS = {
    field_name: "{{{field_name}:0>{max_width}}}".format(field_name=field_name, max_width=field.max_width if field.max_width is not None else 1)
    for field_name, field in NUMBER_FIELDS.items()
}


def __generate_valid_formats(year=2014, month=2, day=3, hour=1, minute=23, second=45, microsecond=123456, tzhour=4, tzminute=30):
    # Given a set of values, generates the 400+ different combinations of those values within a valid ISO 8601 string.
    # Returns a Python format string, the fields in the format string, and the corresponding parameters you could pass to the datetime constructor
    # These can be used by generate_valid_timestamp_and_datetime and generate_invalid_timestamp_and_datetime to produce test cases

    valid_basic_calendar_date_formats = [
        ("{year}{month}{day}", set(["year", "month", "day"]), {"year": year, "month": month, "day": day})
    ]

    valid_extended_calendar_date_formats = [
        ("{year}-{month}", set(["year", "month"]), {"year": year, "month": month, "day": 1}),
        ("{year}-{month}-{day}", set(["year", "month", "day"]), {"year": year, "month": month, "day": day}),
    ]

    valid_date_and_time_separators = [
        None,
        'T',
        't',
        ' '
    ]

    valid_basic_time_formats = [
        ("{hour}", set(["hour"]), {"hour": hour}),
        ("{hour}{minute}", set(["hour", "minute"]), {"hour": hour, "minute": minute}),
        ("{hour}{minute}{second}", set(["hour", "minute", "second"]), {"hour": hour, "minute": minute, "second": second})
    ]

    valid_extended_time_formats = [
        ("{hour}", set(["hour"]), {"hour": hour}),
        ("{hour}:{minute}", set(["hour", "minute"]), {"hour": hour, "minute": minute}),
        ("{hour}:{minute}:{second}", set(["hour", "minute", "second"]), {"hour": hour, "minute": minute, "second": second}),
    ]

    valid_subseconds = [
        ("", set(), {}),
        (".{microsecond}", set(["microsecond"]), {"microsecond": microsecond}),  # TODO: Generate the trimmed 0's version?
        (",{microsecond}", set(["microsecond"]), {"microsecond": microsecond}),
    ]

    valid_tz_info_formats = [
        ("", set(), {}),
        ("Z", set(), {"tzinfo": pytz.UTC}),
        ("z", set(), {"tzinfo": pytz.UTC}),
        ("-{tzhour}", set(["tzhour"]), {"tzinfo": pytz.FixedOffset(-1 * tzhour * 60)}),
        ("+{tzhour}", set(["tzhour"]), {"tzinfo": pytz.FixedOffset(1 * tzhour * 60)}),
        ("-{tzhour}{tzminute}", set(["tzhour", "tzminute"]), {"tzinfo": pytz.FixedOffset(-1 * ((tzhour * 60) + tzminute))}),
        ("+{tzhour}{tzminute}", set(["tzhour", "tzminute"]), {"tzinfo": pytz.FixedOffset(1 * ((tzhour * 60) + tzminute))}),
        ("-{tzhour}:{tzminute}", set(["tzhour", "tzminute"]), {"tzinfo": pytz.FixedOffset(-1 * ((tzhour * 60) + tzminute))}),
        ("+{tzhour}:{tzminute}", set(["tzhour", "tzminute"]), {"tzinfo": pytz.FixedOffset(1 * ((tzhour * 60) + tzminute))})
    ]

    for valid_calendar_date_formats, valid_time_formats in [(valid_basic_calendar_date_formats, valid_basic_time_formats), (valid_extended_calendar_date_formats, valid_extended_time_formats)]:
        for calendar_format, calendar_fields, calendar_params in valid_calendar_date_formats:
            for date_and_time_separator in valid_date_and_time_separators:
                if date_and_time_separator is None:
                    full_format = calendar_format
                    datetime_params = calendar_params
                    yield (full_format, calendar_fields, datetime_params)
                else:
                    for time_format, time_fields, time_params in valid_time_formats:
                        for subsecond_format, subsecond_fields, subsecond_params in valid_subseconds:
                            for tz_info_format, tz_info_fields, tz_info_params in valid_tz_info_formats:
                                if "second" in time_fields:
                                    # Add subsecond
                                    full_format = calendar_format + date_and_time_separator + time_format + subsecond_format + tz_info_format
                                    fields = set().union(calendar_fields, time_fields, subsecond_fields, tz_info_fields)
                                    datetime_params = __merge_dicts(calendar_params, time_params, subsecond_params, tz_info_params)
                                elif subsecond_format == "":  # Arbitrary choice of subsecond format. We don't want duplicates, so we only yield for one of them.
                                    full_format = calendar_format + date_and_time_separator + time_format + tz_info_format
                                    fields = set().union(calendar_fields, time_fields, tz_info_fields)
                                    datetime_params = __merge_dicts(calendar_params, time_params, tz_info_params)
                                else:
                                    # Ignore other subsecond formats
                                    continue

                                yield (full_format, fields, datetime_params)


def __pad_params(**kwargs):
    # Pads parameters to the required field widths.
    return {key: PADDED_NUMBER_FIELD_FORMATS[key].format(**{key: value}) if key in PADDED_NUMBER_FIELD_FORMATS else value for key, value in kwargs.items()}


def generate_valid_timestamp_and_datetime(year=2014, month=2, day=3, hour=1, minute=23, second=45, microsecond=123456, tzhour=4, tzminute=30):
    # Given a set of values, generates the 400+ different combinations of those values within a valid ISO 8601 string, and the corresponding datetime
    # This can be used to generate test cases of valid ISO 8601 timestamps.

    # Note that this will produce many test cases that exercise the exact same code pathways (ie. offer no additional coverage).
    # Given a knowledge of the code, this is excessive, but these serve as a good set of black box tests (ie. You could apply these to any ISO 8601 parse).

    kwargs = {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second,
        "microsecond": microsecond,
        "tzhour": tzhour,
        "tzminute": tzminute
    }
    for timestamp_format, _fields, datetime_params in __generate_valid_formats(**kwargs):
        # Pad each field to the appropriate width
        padded_kwargs = __pad_params(**kwargs)
        timestamp = timestamp_format.format(**padded_kwargs)
        yield (timestamp, datetime.datetime(**datetime_params))


def generate_invalid_timestamp(year=2014, month=2, day=3, hour=1, minute=23, second=45, microsecond=123456, tzhour=4, tzminute=30):
    # At the very least, each field can be invalid in the following ways:
    #   - Have too few characters
    #   - Have too many characters
    #   - Contain invalid characters
    #   - Have a value that is too small
    #   - Have a value that is too large
    #
    # This function takes each valid format (from `__generate_valid_formats()`), and mangles each field within the format to be invalid in each of the above ways.
    # It also tests the case of trailing characters after each format.

    # Note that this will produce many test cases that exercise the exact same code pathways (ie. offer no additional coverage).
    # Given a knowledge of the code, this is excessive, but these serve as a good set of black box tests (ie. You could apply these to any ISO 8601 parse).

    # This does not produce every invalid timestamp format though. For simplicity of the code, it does not cover the cases of:
    #   - The fields having 0 characters (Many fields (like day, minute, second etc.) are optional. So unless the field follows a separator, it is valid to have 0 characters)
    #   - Invalid day numbers for a given month (ex. "2014-02-31")
    #   - Invalid separators (ex. "2014=04=01")
    #   - Missing/Mismatched separators (ex. "2014-0101T0000:00")
    #   - Hour = 24, but not Special midnight case  (ex. "24:00:01")
    #   - Timestamps that bear no resemblance to ISO 8601
    # These cases will need to be test separately

    kwargs = {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second,
        "microsecond": microsecond,
        "tzhour": tzhour,
        "tzminute": tzminute
    }

    for timestamp_format, fields, _datetime_params in __generate_valid_formats(**kwargs):
        for field_name in fields:
            mangled_kwargs = __pad_params(**kwargs)
            field = NUMBER_FIELDS.get(field_name, None)
            if field is not None:
                # Too few characters
                for length in range(1, field.min_width):
                    str_value = str(__pad_params(**{field_name: kwargs[field_name]})[field_name])[0:length]
                    mangled_kwargs[field_name] = "{{:0>{length}}}".format(length=length).format(str_value)
                    timestamp = timestamp_format.format(**mangled_kwargs)
                    yield timestamp

                # Too many characters
                if field.max_width is not None:
                    mangled_kwargs[field_name] = "{{:0>{length}}}".format(length=field.max_width + 1).format(kwargs[field_name])
                    timestamp = timestamp_format.format(**mangled_kwargs)
                    yield timestamp

                # Too small of value
                if (field.min_value - 1) >= 0:
                    mangled_kwargs[field_name] = __pad_params(**{field_name: field.min_value - 1})[field_name]
                    timestamp = timestamp_format.format(**mangled_kwargs)
                    yield timestamp

                # Too large of value
                if field.max_value is not None:
                    mangled_kwargs[field_name] = __pad_params(**{field_name: field.max_value + 1})[field_name]
                    timestamp = timestamp_format.format(**mangled_kwargs)
                    yield timestamp

                # Invalid characters
                max_invalid_characters = field.max_width if field.max_width is not None else 1
                # ex. 2014 -> a, aa, aaa
                for length in range(1, max_invalid_characters):
                    mangled_kwargs[field_name] = "a" * length
                    timestamp = timestamp_format.format(**mangled_kwargs)
                    yield timestamp
                # ex. 2014 -> aaaa, 2aaa, 20aa, 201a
                for length in range(0, max_invalid_characters):
                    str_value = str(__pad_params(**{field_name: kwargs[field_name]})[field_name])[0:length]
                    mangled_kwargs[field_name] = "{{:a<{length}}}".format(length=max_invalid_characters).format(str_value)
                    timestamp = timestamp_format.format(**mangled_kwargs)
                    yield timestamp

        # Trailing characters
        timestamp = timestamp_format.format(**__pad_params(**kwargs)) + "EXTRA"
        yield timestamp
