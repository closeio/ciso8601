import ciso8601
import datetime
from generate_test_timestamps import generate_valid_timestamp_and_datetime, generate_invalid_timestamp

import sys  # TODO: Clean this up
if sys.version_info.major == 2:
    import unittest2 as unittest
else:
    import unittest


class ValidTimestampTestCase(unittest.TestCase):
    def test_auto_generated_valid_formats(self):
        for (timestamp, expected_datetime) in generate_valid_timestamp_and_datetime():
            try:
                self.assertEqual(ciso8601.parse_datetime(timestamp), expected_datetime)
            except Exception:
                print("Had problems parsing: {timestamp}".format(timestamp=timestamp))
                raise

    def test_parse_as_naive_auto_generated_valid_formats(self):
        for (timestamp, expected_datetime) in generate_valid_timestamp_and_datetime():
            try:
                self.assertEqual(ciso8601.parse_datetime_as_naive(timestamp), expected_datetime.replace(tzinfo=None))
            except Exception:
                print("Had problems parsing: {timestamp}".format(timestamp=timestamp))
                raise

    def test_excessive_subsecond_precision(self):
        self.assertEqual(
            ciso8601.parse_datetime('20140203T103527.234567891234'),
            datetime.datetime(2014, 2, 3, 10, 35, 27, 234567)
        )

    def test_leap_year(self):
        # There is nothing unusual about leap years in ISO 8601.
        # We just want to make sure that they work in general.
        for leap_year in (1600, 2000, 2016):
            self.assertEqual(
                ciso8601.parse_datetime('{}-02-29'.format(leap_year)),
                datetime.datetime(leap_year, 2, 29, 0, 0, 0, 0)
            )

    def test_special_midnight(self):
        self.assertEqual(
            ciso8601.parse_datetime('2014-02-03T24:00:00'),
            datetime.datetime(2014, 2, 4, 0, 0, 0)
        )


class InvalidTimestampTestCase(unittest.TestCase):
    # Many invalid test cases are covered by `test_parse_auto_generated_invalid_formats`,
    # But it doesn't cover all invalid cases, so we test those here.
    # See `generate_test_timestamps.generate_invalid_timestamp` for details.

    def test_parse_auto_generated_invalid_formats(self):
        for timestamp in generate_invalid_timestamp():
            with self.assertRaises(ValueError, msg="Timestamp '{0}' was supposed to be invalid, but parsing it didn't raise ValueError.".format(timestamp)):
                ciso8601.parse_datetime(timestamp)

    def test_invalid_calendar_separator(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing month",
            ciso8601.parse_datetime,
            '2018=01=01',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing date separator \('-'\) \('=', Index: 7\)",
            ciso8601.parse_datetime,
            '2018-01=01',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing date separator \('-'\) \('0', Index: 7\)",
            ciso8601.parse_datetime,
            '2018-0101',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing day \('-', Index: 6\)",
            ciso8601.parse_datetime,
            '201801-01',
        )

    def test_invalid_empty_but_required_fields(self):
        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing year. Expected 4 more characters",
            ciso8601.parse_datetime,
            '',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing month. Expected 2 more characters",
            ciso8601.parse_datetime,
            '2018-',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing day. Expected 2 more characters",
            ciso8601.parse_datetime,
            '2018-01-',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing hour. Expected 2 more characters",
            ciso8601.parse_datetime,
            '2018-01-01T',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing minute. Expected 2 more characters",
            ciso8601.parse_datetime,
            '2018-01-01T00:',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing second. Expected 2 more characters",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing subsecond. Expected 1 more character",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing tz hour. Expected 2 more characters",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00+',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing tz minute. Expected 2 more characters",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00-00:',
        )

    def test_invalid_day_for_month(self):
        for non_leap_year in (1700, 1800, 1900, 2014):
            self.assertRaisesRegex(
                ValueError,
                r"day is out of range for month",
                ciso8601.parse_datetime,
                '{}-02-29'.format(non_leap_year)
            )

        self.assertRaisesRegex(
            ValueError,
            r"day is out of range for month",
            ciso8601.parse_datetime,
            '2014-01-32',
        )

        self.assertRaisesRegex(
            ValueError,
            r"day is out of range for month",
            ciso8601.parse_datetime,
            '2014-06-31',
        )

        self.assertRaisesRegex(
            ValueError,
            r"day is out of range for month",
            ciso8601.parse_datetime,
            '2014-06-00',
        )

    def test_invalid_yyyymm_format(self):
        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing day. Expected 2 more characters",
            ciso8601.parse_datetime,
            '201406',
        )

    def test_invalid_date_and_time_separator(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing date and time separator \(ie. 'T' or ' '\) \('_', Index: 10\)",
            ciso8601.parse_datetime,
            '2018-01-01_00:00:00',
        )
    def test_invalid_hour_24(self):
        # A value of hour = 24 is only valid in the special case of 24:00:00
        self.assertRaisesRegex(
            ValueError,
            r"hour must be in 0..23",
            ciso8601.parse_datetime,
            '20140203T24:35:27',
        )
        self.assertEqual(
            ciso8601.parse_datetime('2014-12-05T00:00+23:59'),
            datetime.datetime(2014, 12, 5, 0, 0, 0, 0, pytz.FixedOffset(1439))
        )
        self.assertEqual(
            ciso8601.parse_datetime('2014-12-05T00:00-23:59'),
            datetime.datetime(2014, 12, 5, 0, 0, 0, 0, pytz.FixedOffset(-1439))
        )

    def test_invalid_time_separator(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing time separator \(':'\) \('=', Index: 16\)",
            ciso8601.parse_datetime,
            '2018-01-01T00:00=00'
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing time separator \(':'\) \('0', Index: 16\)",
            ciso8601.parse_datetime,
            '2018-01-01T00:0000'
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing second \(':', Index: 15\)",
            ciso8601.parse_datetime,
            '2018-01-01T0000:00'
        )

    def test_invalid_tz_minute(self):
        # TODO: Determine whether this is a valid ISO 8601 value and therefore whether ciso8601 should support it.
        self.assertRaisesRegex(
            ValueError,
            r"tzminute must be in 0..59",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00-00:99',
        )

    def test_invalid_tz_offsets_too_large(self):
        # The Python interpreter crashes if you give the datetime constructor a TZ offset with an absolute value >= 1440
        # TODO: Determine whether these are valid ISO 8601 values and therefore whether ciso8601 should support them.
        self.assertRaisesRegex(
            ValueError,
            r"Absolute tz offset is too large \(-5940\)",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00-99',
        )

        self.assertRaisesRegex(
            ValueError,
            r"tzminute must be in 0..59",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00-23:60',
        )


class GithubIssueRegressionTestCase(unittest.TestCase):
    # These are test cases that were provided in GitHub issues submitted to ciso8601.
    # They are kept here as regression tests.
    # They might not have any additional value above-and-beyond what is already tested in the normal unit tests.

    def test_issue_5(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing minute \(':', Index: 12\)",
            ciso8601.parse_datetime,
            '20140203T10::27',
        )

    def test_issue_6(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing second \('.', Index: 15\)",
            ciso8601.parse_datetime,
            '20140203 04:05:.123456',
        )

    def test_issue_8(self):
        self.assertRaisesRegex(
            ValueError,
            r"hour must be in 0..23",
            ciso8601.parse_datetime,
            '2001-01-01T24:01:01',
        )

        self.assertRaisesRegex(
            ValueError,
            r"month must be in 1..12",
            ciso8601.parse_datetime,
            '07722968',
        )

    def test_issue_13(self):
        self.assertRaisesRegex(
            ValueError,
            r"month must be in 1..12",
            ciso8601.parse_datetime,
            '2014-13-01',
        )
        
    def test_issue_22(self):
        self.assertRaisesRegex(
            ValueError,
            r"day is out of range for month",
            ciso8601.parse_datetime,
            '2016-11-31T12:34:34.521059',
        )

    def test_issue_35(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing date separator \('-'\) \('1', Index: 7\)",
            ciso8601.parse_datetime,
            '2017-0012-27T13:35:19+0200',
        )

    def test_issue_42(self):
        self.assertRaisesRegex(
            ValueError,
            r"day is out of range for month",
            ciso8601.parse_datetime,
            '20140200',
        )


if __name__ == '__main__':
    unittest.main()
