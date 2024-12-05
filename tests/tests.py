# -*- coding: utf-8 -*-

import copy
import datetime
import pickle
import platform
import re
import sys
import unittest

from ciso8601 import _hard_coded_benchmark_timestamp, FixedOffset, parse_datetime, parse_datetime_as_naive, parse_rfc3339
from generate_test_timestamps import generate_valid_timestamp_and_datetime, generate_invalid_timestamp

if sys.version_info.major == 2:
    # We use add `unittest.TestCase.assertRaisesRegex` method, which is called `assertRaisesRegexp` in Python 2.
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp


class ValidTimestampTestCase(unittest.TestCase):
    def test_auto_generated_valid_formats(self):
        for (timestamp, expected_datetime) in generate_valid_timestamp_and_datetime():
            try:
                self.assertEqual(parse_datetime(timestamp), expected_datetime)
            except Exception:
                print("Had problems parsing: {timestamp}".format(timestamp=timestamp))
                raise

    def test_parse_as_naive_auto_generated_valid_formats(self):
        for (timestamp, expected_datetime) in generate_valid_timestamp_and_datetime():
            try:
                self.assertEqual(parse_datetime_as_naive(timestamp), expected_datetime.replace(tzinfo=None))
            except Exception:
                print("Had problems parsing: {timestamp}".format(timestamp=timestamp))
                raise

    def test_excessive_subsecond_precision(self):
        self.assertEqual(
            parse_datetime("20140203T103527.234567891234"),
            datetime.datetime(2014, 2, 3, 10, 35, 27, 234567),
        )

    def test_leap_year(self):
        # There is nothing unusual about leap years in ISO 8601.
        # We just want to make sure that they work in general.
        for leap_year in (1600, 2000, 2016):
            self.assertEqual(
                parse_datetime("{}-02-29".format(leap_year)),
                datetime.datetime(leap_year, 2, 29, 0, 0, 0, 0),
            )

    def test_special_midnight(self):
        self.assertEqual(
            parse_datetime("2014-02-03T24:00:00"),
            datetime.datetime(2014, 2, 4, 0, 0, 0),
        )

    def test_returns_built_in_utc_if_available(self):
        # Python 3.7 added a built-in UTC object at the C level (`PyDateTime_TimeZone_UTC`)
        # PyPy added support for it in 7.3.6, but only for PyPy 3.8+

        timestamp = '2018-01-01T00:00:00.00Z'
        if sys.version_info >= (3, 7) and \
            (platform.python_implementation() == 'CPython'
             or (platform.python_implementation() == 'PyPy' and sys.version_info >= (3, 8) and sys.pypy_version_info >= (7, 3, 6))):
            self.assertIs(parse_datetime(timestamp).tzinfo, datetime.timezone.utc)
        else:
            self.assertIsInstance(parse_datetime(timestamp).tzinfo, FixedOffset)

    def test_ordinal(self):
        self.assertEqual(
            parse_datetime("2014-001"),
            datetime.datetime(2014, 1, 1, 0, 0, 0),
        )
        self.assertEqual(
            parse_datetime("2014-031"),
            datetime.datetime(2014, 1, 31, 0, 0, 0),
        )
        self.assertEqual(
            parse_datetime("2014-032"),
            datetime.datetime(2014, 2, 1, 0, 0, 0),
        )
        self.assertEqual(
            parse_datetime("2014-059"),
            datetime.datetime(2014, 2, 28, 0, 0, 0),
        )
        self.assertEqual(
            parse_datetime("2014-060"),
            datetime.datetime(2014, 3, 1, 0, 0, 0),
        )
        self.assertEqual(
            parse_datetime("2016-060"), # Leap year
            datetime.datetime(2016, 2, 29, 0, 0, 0),
        )
        self.assertEqual(
            parse_datetime("2014-365"),
            datetime.datetime(2014, 12, 31, 0, 0, 0),
        )
        self.assertEqual(
            parse_datetime("2016-365"), # Leap year
            datetime.datetime(2016, 12, 30, 0, 0, 0),
        )
        self.assertEqual(
            parse_datetime("2016-366"), # Leap year
            datetime.datetime(2016, 12, 31, 0, 0, 0),
        )

class InvalidTimestampTestCase(unittest.TestCase):
    # Many invalid test cases are covered by `test_parse_auto_generated_invalid_formats`,
    # But it doesn't cover all invalid cases, so we test those here.
    # See `generate_test_timestamps.generate_invalid_timestamp` for details.

    def test_parse_auto_generated_invalid_formats(self):
        for timestamp, reason in generate_invalid_timestamp():
            try:
                with self.assertRaises(ValueError, msg="Timestamp '{0}' was supposed to be invalid ({1}), but parsing it didn't raise ValueError.".format(timestamp, reason)):
                    parse_datetime(timestamp)
            except Exception as exc:
                print("Timestamp '{0}' was supposed to raise ValueError ({1}), but raised {2} instead".format(timestamp, reason, type(exc).__name__))
                raise

    def test_non_ascii_characters(self):
        if sys.version_info >= (3, 3):
            self.assertRaisesRegex(
                ValueError,
                r"Invalid character while parsing date and time separator \(i.e., 'T', 't', or ' '\) \('🐵', Index: 10\)",
                parse_datetime,
                "2019-01-01🐵01:02:03Z",
            )
            self.assertRaisesRegex(
                ValueError,
                r"Invalid character while parsing day \('🐵', Index: 8\)",
                parse_datetime,
                "2019-01-🐵",
            )
        else:
            self.assertRaisesRegex(
                ValueError,
                r"Invalid character while parsing ordinal day \(Index: 7\)",
                parse_datetime,
                "2019-01🐵01",
            )
            self.assertRaisesRegex(
                ValueError,
                r"Invalid character while parsing day \(Index: 8\)",
                parse_datetime,
                "2019-01-🐵",
            )

    def test_invalid_calendar_separator(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing month",
            parse_datetime,
            "2018=01=01",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing ordinal day \('=', Index: 7\)",
            parse_datetime,
            "2018-01=01",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing date and time separator \(i.e., 'T', 't', or ' '\) \('2', Index: 8\)",
            parse_datetime,
            "2018-0102",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing ordinal day \('-', Index: 6\)",
            parse_datetime,
            "201801-01",
        )

    def test_invalid_empty_but_required_fields(self):
        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing year. Expected 4 more characters",
            parse_datetime,
            "",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing month. Expected 2 more characters",
            parse_datetime,
            "2018-",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing day. Expected 2 more characters",
            parse_datetime,
            "2018-01-",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing hour. Expected 2 more characters",
            parse_datetime,
            "2018-01-01T",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing minute. Expected 2 more characters",
            parse_datetime,
            "2018-01-01T00:",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing second. Expected 2 more characters",
            parse_datetime,
            "2018-01-01T00:00:",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing subsecond. Expected 1 more character",
            parse_datetime,
            "2018-01-01T00:00:00.",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing tz hour. Expected 2 more characters",
            parse_datetime,
            "2018-01-01T00:00:00.00+",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing tz minute. Expected 2 more characters",
            parse_datetime,
            "2018-01-01T00:00:00.00-00:",
        )

    def test_invalid_day_for_month(self):
        if platform.python_implementation() == 'PyPy' and sys.version_info.major >= 3:
            for non_leap_year in (1700, 1800, 1900, 2014):
                self.assertRaisesRegex(
                    ValueError,
                    r"('day must be in 1..28', 29)",
                    parse_datetime,
                    "{}-02-29".format(non_leap_year),
                )

            self.assertRaisesRegex(
                ValueError,
                r"('day must be in 1..31', 32)",
                parse_datetime,
                "2014-01-32",
            )

            self.assertRaisesRegex(
                ValueError,
                r"('day must be in 1..30', 31)",
                parse_datetime,
                "2014-06-31",
            )

            self.assertRaisesRegex(
                ValueError,
                r"('day must be in 1..30', 0)",
                parse_datetime,
                "2014-06-00",
            )
        else:
            for non_leap_year in (1700, 1800, 1900, 2014):
                self.assertRaisesRegex(
                    ValueError,
                    r"day is out of range for month",
                    parse_datetime,
                    "{}-02-29".format(non_leap_year),
                )

            self.assertRaisesRegex(
                ValueError,
                r"day is out of range for month",
                parse_datetime,
                "2014-01-32",
            )

            self.assertRaisesRegex(
                ValueError,
                r"day is out of range for month",
                parse_datetime,
                "2014-06-31",
            )

            self.assertRaisesRegex(
                ValueError,
                r"day is out of range for month",
                parse_datetime,
                "2014-06-00",
            )

    def test_invalid_ordinal(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid ordinal day: 0 is too small",
            parse_datetime,
            "2014-000",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid ordinal day: 0 is too small",
            parse_datetime,
            "2014000",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid ordinal day: 366 is too large for year 2014",
            parse_datetime,
            "2014-366", # Not a leap year
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid ordinal day: 366 is too large for year 2014",
            parse_datetime,
            "2014366", # Not a leap year
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid ordinal day: 999 is too large for year 2014",
            parse_datetime,
            "2014-999",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid ordinal day: 999 is too large for year 2014",
            parse_datetime,
            "2014999",
        )

    def test_invalid_yyyymm_format(self):
        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing ordinal day. Expected 1 more character",
            parse_datetime,
            "201406",
        )

    def test_invalid_date_and_time_separator(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing date and time separator \(i.e., 'T', 't', or ' '\) \('_', Index: 10\)",
            parse_datetime,
            "2018-01-01_00:00:00",
        )

    def test_invalid_hour_24(self):
        # A value of hour = 24 is only valid in the special case of 24:00:00
        self.assertRaisesRegex(
            ValueError,
            r"hour must be in 0..23",
            parse_datetime,
            "2014-02-03T24:35:27",
        )

    def test_invalid_time_separator(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing time separator \(':'\) \('=', Index: 16\)",
            parse_datetime,
            "2018-01-01T00:00=00",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing time separator \(':'\) \('0', Index: 16\)",
            parse_datetime,
            "2018-01-01T00:0000",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing second \(':', Index: 15\)",
            parse_datetime,
            "2018-01-01T0000:00",
        )

    def test_invalid_tz_minute(self):
        self.assertRaisesRegex(
            ValueError,
            r"tzminute must be in 0..59",
            parse_datetime,
            "2018-01-01T00:00:00.00-00:99",
        )

    def test_invalid_tz_offsets_too_large(self):
        # The TZ offsets with an absolute value >= 1440 minutes are not supported by the tzinfo spec.
        # See https://docs.python.org/3/library/datetime.html#datetime.tzinfo.utcoffset

        invalid_offsets = [("-24", -1440), ("+24", 1440), ("-99", -5940), ("+99", 5940)]
        for offset_string, offset_minutes in invalid_offsets:
            # Error message differs whether or not we are using pytz or datetime.timezone
            # (and also by which Python version. Python 3.7 has different timedelta.repr())
            # Of course we no longer use either, but for backwards compatibility
            # with v2.0.x, we did not change the error messages.
            if sys.version_info.major >= 3:
                expected_error_message = re.escape("offset must be a timedelta strictly between -timedelta(hours=24) and timedelta(hours=24), not {0}.".format(repr(datetime.timedelta(minutes=offset_minutes))))
            else:
                expected_error_message = re.escape("'absolute offset is too large', {0}".format(offset_minutes))

            self.assertRaisesRegex(
                ValueError,
                expected_error_message,
                parse_datetime,
                "2018-01-01T00:00:00.00{0}".format(offset_string),
            )

        self.assertRaisesRegex(
            ValueError,
            r"tzminute must be in 0..59",
            parse_datetime,
            "2018-01-01T00:00:00.00-23:60",
        )

    def test_mixed_basic_and_extended_formats(self):
        """
        Both dates and times have "basic" and "extended" formats.
        But when you combine them into a datetime, the date and time components
        must have the same format.
        """
        self.assertRaisesRegex(
            ValueError,
            r"Cannot combine \"extended\" date format with \"basic\" time format",
            parse_datetime,
            "2014-01-02T010203",
        ),

        self.assertRaisesRegex(
            ValueError,
            r"Cannot combine \"basic\" date format with \"extended\" time format",
            parse_datetime,
            "20140102T01:02:03",
        )

    def test_bce_years(self):
        """
        These are technically valid ISO 8601 datetimes.
        However, cPython cannot support values non-positive year values
        """
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing year \('-', Index: 0\). While valid ISO 8601 years, BCE years are not supported by Python's `datetime` objects.",
            parse_datetime,
            "-2014-01-02",
        )

class Rfc3339TestCase(unittest.TestCase):
    def test_valid_rfc3339_timestamps(self):
        """
        Validate that valid RFC 3339 datetimes are parseable by parse_rfc3339
        and produce the same result as parse_datetime.
        """
        for string in [
            "2018-01-02T03:04:05Z",
            "2018-01-02t03:04:05z",
            "2018-01-02 03:04:05z",
            "2018-01-02T03:04:05+00:00",
            "2018-01-02T03:04:05-00:00",
            "2018-01-02T03:04:05.12345Z",
            "2018-01-02T03:04:05+01:23",
            "2018-01-02T03:04:05-12:34",
            "2018-01-02T03:04:05-12:34",
        ]:
            self.assertEqual(
                parse_datetime(string), parse_rfc3339(string)
            )

    def test_invalid_rfc3339_timestamps(self):
        """
        Validate that datetime strings that are valid ISO 8601 but invalid RFC
        3339 trigger a ValueError when passed to RFC 3339, and that this
        ValueError explicitly mentions RFC 3339.
        """
        for timestamp in [
            "2018-01-02",  # Missing mandatory time
            "2018-01-02T03",  # Missing mandatory minute and second
            "2018-01-02T03Z",  # Missing mandatory minute and second
            "2018-01-02T03:04",  # Missing mandatory minute and second
            "2018-01-02T03:04Z",  # Missing mandatory minute and second
            "2018-01-02T03:04:01+04",  # Missing mandatory offset minute
            "2018-01-02T03:04:05",  # Missing mandatory offset
            "2018-01-02T03:04:05.12345",  # Missing mandatory offset
            "2018-01-02T24:00:00Z",  # 24:00:00 is not valid in RFC 3339
            "20180102T03:04:05-12:34",  # Missing mandatory date separators
            "2018-01-02T030405-12:34",  # Missing mandatory time separators
            "2018-01-02T03:04:05-1234",  # Missing mandatory offset separator
            "2018-01-02T03:04:05,12345Z",  # Invalid comma fractional second separator
        ]:
            with self.assertRaisesRegex(ValueError, r"RFC 3339", msg="Timestamp '{0}' was supposed to be invalid, but parsing it didn't raise ValueError.".format(timestamp)):
                parse_rfc3339(timestamp)


class FixedOffsetTestCase(unittest.TestCase):
    def test_all_valid_offsets(self):
        [FixedOffset(i * 60) for i in range(-1439, 1440)]

    def test_offsets_outside_valid_range(self):
        invalid_offsets = [-1440, 1440, 10000, -10000]
        for invalid_offset in invalid_offsets:
            with self.assertRaises(ValueError, msg="Fixed offset of {0} minutes was supposed to be invalid, but it didn't raise ValueError.".format(invalid_offset)):
                FixedOffset(invalid_offset * 60)


class PicklingTestCase(unittest.TestCase):
    # Found as a result of https://github.com/movermeyer/backports.datetime_fromisoformat/issues/12
    def test_basic_pickle_and_copy(self):
        dt = parse_datetime('2018-11-01 20:42:09')
        dt2 = pickle.loads(pickle.dumps(dt))
        self.assertEqual(dt, dt2)
        dt3 = copy.deepcopy(dt)
        self.assertEqual(dt, dt3)

        # FixedOffset
        dt = parse_datetime('2018-11-01 20:42:09+01:30')
        dt2 = pickle.loads(pickle.dumps(dt))
        self.assertEqual(dt, dt2)
        dt3 = copy.deepcopy(dt)
        self.assertEqual(dt, dt3)


class GithubIssueRegressionTestCase(unittest.TestCase):
    # These are test cases that were provided in GitHub issues submitted to ciso8601.
    # They are kept here as regression tests.
    # They might not have any additional value above-and-beyond what is already tested in the normal unit tests.

    def test_issue_5(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing minute \(':', Index: 14\)",
            parse_datetime,
            "2014-02-03T10::27",
        )

    def test_issue_6(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing second \('.', Index: 17\)",
            parse_datetime,
            "2014-02-03 04:05:.123456",
        )

    def test_issue_8(self):
        self.assertRaisesRegex(
            ValueError,
            r"hour must be in 0..23",
            parse_datetime,
            "2001-01-01T24:01:01",
        )

        self.assertRaisesRegex(
            ValueError,
            r"month must be in 1..12",
            parse_datetime,
            "07722968",
        )

    def test_issue_13(self):
        self.assertRaisesRegex(
            ValueError,
            r"month must be in 1..12",
            parse_datetime,
            "2014-13-01",
        )

    def test_issue_22(self):
        if platform.python_implementation() == 'PyPy' and sys.version_info.major >= 3:
            self.assertRaisesRegex(
                ValueError,
                r"('day must be in 1..30', 31)",
                parse_datetime,
                "2016-11-31T12:34:34.521059",
            )
        else:
            self.assertRaisesRegex(
                ValueError,
                r"day is out of range for month",
                parse_datetime,
                "2016-11-31T12:34:34.521059",
            )

    def test_issue_35(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing date and time separator \(i.e., 'T', 't', or ' '\) \('2', Index: 8\)",
            parse_datetime,
            "2017-0012-27T13:35:19+0200",
        )

    def test_issue_42(self):
        if platform.python_implementation() == 'PyPy' and sys.version_info.major >= 3:
            self.assertRaisesRegex(
                ValueError,
                r"('day must be in 1..28', 0)",
                parse_datetime,
                "20140200",
            )
        else:
            self.assertRaisesRegex(
                ValueError,
                r"day is out of range for month",
                parse_datetime,
                "20140200",
            )

    def test_issue_71(self):
        self.assertRaisesRegex(
            ValueError,
            r"Cannot combine \"basic\" date format with \"extended\" time format",
            parse_datetime,
            "20010203T04:05:06Z",
        )

        self.assertRaisesRegex(
            ValueError,
            r"Cannot combine \"basic\" date format with \"extended\" time format",
            parse_datetime,
            "20010203T04:05",
        )


class HardCodedBenchmarkTimestampTestCase(unittest.TestCase):
    def test_returns_expected_hardcoded_datetime(self):
        self.assertEqual(
            _hard_coded_benchmark_timestamp(),
            datetime.datetime(2014, 1, 9, 21, 48, 0, 0),
        )

if __name__ == "__main__":
    unittest.main()
