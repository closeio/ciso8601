import ciso8601
import datetime
import pytz


import sys  # TODO: Clean this up
if sys.version_info.major == 2:
    import unittest2 as unittest
else:
    import unittest


class CISO8601TestCase(unittest.TestCase):
    def test_formats(self):
        expected = datetime.datetime(2014, 2, 3)
        self.assertEqual(
            ciso8601.parse_datetime('20140203'),
            expected
        )
        self.assertEqual(
            ciso8601.parse_datetime('2014-02-03'),
            expected
        )

        self.assertEqual(
            ciso8601.parse_datetime('2014-02'),
            datetime.datetime(2014, 2, 1)
        )

        self.assertEqual(
            ciso8601.parse_datetime('2014-02T05'),
            datetime.datetime(2014, 2, 1, 5)
        )

        self.assertEqual(
            ciso8601.parse_datetime('20140203T1035'),
            datetime.datetime(2014, 2, 3, 10, 35)
        )

        self.assertEqual(
            ciso8601.parse_datetime('20140203T10:35'),
            datetime.datetime(2014, 2, 3, 10, 35)
        )

        self.assertEqual(
            ciso8601.parse_datetime('20140203T103527'),
            datetime.datetime(2014, 2, 3, 10, 35, 27)
        )

        self.assertEqual(
            ciso8601.parse_datetime('20140203T10:35:27'),
            datetime.datetime(2014, 2, 3, 10, 35, 27)
        )

        self.assertEqual(
            ciso8601.parse_datetime('20140203T10:35:27.234'),
            datetime.datetime(2014, 2, 3, 10, 35, 27, 234000)
        )

        self.assertEqual(
            ciso8601.parse_datetime('20140203T103527,234567'),
            datetime.datetime(2014, 2, 3, 10, 35, 27, 234567)
        )

        self.assertEqual(
            ciso8601.parse_datetime('20140203T103527.234567891234'),
            datetime.datetime(2014, 2, 3, 10, 35, 27, 234567)
        )
        for leap_year in (1600, 2000, 2016):
            self.assertEqual(
                ciso8601.parse_datetime('{}-02-29'.format(leap_year)),
                datetime.datetime(leap_year, 2, 29, 0, 0, 0, 0)
            )

    def test_aware_utc(self):
        expected = datetime.datetime(2014, 12, 5, 12, 30, 45, 123456, pytz.UTC)
        self.assertEqual(
            ciso8601.parse_datetime('2014-12-05T12:30:45.123456Z'),
            expected
        )
        self.assertEqual(
            ciso8601.parse_datetime('2014-12-05T12:30:45.123456+00:00'),
            expected,
        )
        self.assertEqual(
            ciso8601.parse_datetime('2014-12-05T12:30:45.123456-00:00'),
            expected,
        )

    def test_aware_offset(self):
        self.assertEqual(
            ciso8601.parse_datetime('2014-12-05T12:30:45.123456+05:30'),
            datetime.datetime(2014, 12, 5, 12, 30, 45, 123456, pytz.FixedOffset(330))
        )
        self.assertEqual(
            ciso8601.parse_datetime('2014-12-05T12:30:45.123456-05:30'),
            datetime.datetime(2014, 12, 5, 12, 30, 45, 123456, pytz.FixedOffset(-330))
        )
        self.assertEqual(
            ciso8601.parse_datetime('2014-12-05T12:30:45.123456-06:00'),
            datetime.datetime(2014, 12, 5, 12, 30, 45, 123456, pytz.FixedOffset(-360))
        )

    def test_invalid_year(self):
        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing year. Expected 4 more characters",
            ciso8601.parse_datetime,
            '',
        )
        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing year. Expected 3 more characters",
            ciso8601.parse_datetime,
            '2',
        )
        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing year. Expected 2 more characters",
            ciso8601.parse_datetime,
            '20',
        )
        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing year. Expected 1 more character",
            ciso8601.parse_datetime,
            '201',
        )
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing year",
            ciso8601.parse_datetime,
            'asdf',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing year",
            ciso8601.parse_datetime,
            'Z',
        )

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

    def test_invalid_month(self):
        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing month. Expected 2 more characters",
            ciso8601.parse_datetime,
            '2018-',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing month. Expected 1 more character",
            ciso8601.parse_datetime,
            '2018-1',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing month",
            ciso8601.parse_datetime,
            '2018-a',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing month",
            ciso8601.parse_datetime,
            '2018-0a',
        )

        self.assertRaisesRegex(
            ValueError,
            r"month must be in 1..12",
            ciso8601.parse_datetime,
            '2014-99-03',
        )

        self.assertRaisesRegex(
            ValueError,
            r"month must be in 1..12",
            ciso8601.parse_datetime,
            '2014-13-03',
        )

        self.assertRaisesRegex(
            ValueError,
            r"month must be in 1..12",
            ciso8601.parse_datetime,
            '2014-00-03',
        )

    def test_invalid_day(self):
        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing day. Expected 2 more characters",
            ciso8601.parse_datetime,
            '2018-01-',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing day",
            ciso8601.parse_datetime,
            '2018-01-a',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing day",
            ciso8601.parse_datetime,
            '2018-01-0a',
        )

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

    def test_invalid_date_and_time_delimiter(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing date and time separator \(ie. 'T' or ' '\) \('_', Index: 10\)",
            ciso8601.parse_datetime,
            '2018-01-01_00:00:00',
        )

    def test_invalid_hour(self):

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing hour. Expected 2 more characters",
            ciso8601.parse_datetime,
            '2018-01-01T',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing hour. Expected 1 more character",
            ciso8601.parse_datetime,
            '2018-01-01T0',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing hour",
            ciso8601.parse_datetime,
            '2018-01-01Ta',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing hour",
            ciso8601.parse_datetime,
            '2018-01-01T0a',
        )

        self.assertRaisesRegex(
            ValueError,
            r"hour must be in 0..23",
            ciso8601.parse_datetime,
            '2018-01-01T99',
        )

        self.assertRaisesRegex(
            ValueError,
            r"hour must be in 0..23",
            ciso8601.parse_datetime,
            '20140203T24:35:27',
        )

    def test_invalid_minute(self):

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing minute. Expected 2 more characters",
            ciso8601.parse_datetime,
            '2018-01-01T00:',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing minute. Expected 1 more character",
            ciso8601.parse_datetime,
            '2018-01-01T00:1',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing minute",
            ciso8601.parse_datetime,
            '2018-01-01T00:a',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing minute",
            ciso8601.parse_datetime,
            '2018-01-01T00:0a',
        )

        self.assertRaisesRegex(
            ValueError,
            r"minute must be in 0..59",
            ciso8601.parse_datetime,
            '2018-01-01T00:99',
        )

        self.assertRaisesRegex(
            ValueError,
            r"minute must be in 0..59",
            ciso8601.parse_datetime,
            '20140203T23:60:27',
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

    def test_invalid_second(self):

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing second. Expected 2 more characters",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing second. Expected 1 more character",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:1',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing second",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:a',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing second",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:1a',
        )

        self.assertRaisesRegex(
            ValueError,
            r"second must be in 0..59",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:99',
        )

        self.assertRaisesRegex(
            ValueError,
            r"second must be in 0..59",
            ciso8601.parse_datetime,
            '20140203T23:35:61',
        )

    def test_invalid_subsecond(self):
        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing subsecond. Expected 1 more character",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing subsecond \('a', Index: 20\)",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.a',
        )

    def test_invalid_tz_hour(self):
        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing tz hour. Expected 1 more character",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00-0',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing tz hour \('a', Index: 24\)",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00-0a',
        )

    def test_invalid_tz_minute(self):

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing tz minute. Expected 2 more characters",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00-00:',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing tz minute \('a', Index: 25\)",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00-00a',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing tz minute \('a', Index: 26\)",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00-00:a',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Unexpected end of string while parsing tz minute. Expected 1 more character",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00-00:0',
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing tz minute \('a', Index: 27\)",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00-00:0a',
        )

    def test_tz_offsets_too_large(self):
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
            r"Absolute tz offset is too large \(-1440\)",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00-23:60',
        )

    def test_invalid_trailing_characters(self):
        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing date and time separator \(ie. 'T' or ' '\) \('a', Index: 10\)",
            ciso8601.parse_datetime,
            '2014-12-05asdfasdf'
        )

        self.assertRaisesRegex(
            ValueError,
            r"Invalid character while parsing minute \('a', Index: 13\)",
            ciso8601.parse_datetime,
            '2018-01-01T00a',
        )

        self.assertRaisesRegex(
            ValueError,
            r"unconverted data remains: 'a'",
            ciso8601.parse_datetime,
            '2014-01-01T00:00:00Za',
        )

        self.assertRaisesRegex(
            ValueError,
            r"unconverted data remains: 'a'",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00.00-00:00a',
        )

        self.assertRaisesRegex(
            ValueError,
            r"unconverted data remains: 'a'",
            ciso8601.parse_datetime,
            '2018-01-01T00:00:00a',
        )

    def test_others(self):
        # These are tests that previously existed. They may or may not have any additional value.
        parse = ciso8601.parse_datetime

        def check(s, *result):
            if (
                len(result) == 1 and
                isinstance(result[0], type) and
                issubclass(result[0], Exception)
            ):
                self.assertRaises(result[0], parse, s)
            else:
                self.assertEqual(parse(s), datetime.datetime(*result))

        check('20140203 04:05:06.123', 2014, 2, 3, 4, 5, 6, 123000)
        check('20140203 04:05:06,123', 2014, 2, 3, 4, 5, 6, 123000)
        check('20140203 04:05:0.123', ValueError)
        check('20140203 04:05:.123', ValueError)
        check('20140203 04:05:,123', ValueError)
        check('20140203 04:05:06.', ValueError)
        check('20140203 0405:06.', ValueError)
        check('20140203 040506.', ValueError)
        check('20140203 04050.', ValueError)
        check('20140203 0405:0', ValueError)
        check('20140203 04:05:.', ValueError)
        check('20140203 04:05:,', ValueError)
        check('20140203 04::', ValueError)
        check('20140203 04:00:', ValueError)
        check('20140203 04::01', ValueError)
        check('20140203 04:', ValueError)

        check('2014-02-03', 2014, 2, 3)
        check('2014-0-03', ValueError)
        check('2014--03', ValueError)
        check('2014-02', 2014, 2, 1)
        check('2014--0', ValueError)
        check('2014--', ValueError)
        check('2014-', ValueError)
        check('2014', ValueError)

        check('20140203 040506.123', 2014, 2, 3, 4, 5, 6, 123000)
        check('20140203 040506123', ValueError)
        check('20140203 04050612', ValueError)
        check('20140203 0405061', ValueError)
        check('20140203 040506', 2014, 2, 3, 4, 5, 6)
        check('20140203 04050', ValueError)
        check('20140203 0405', 2014, 2, 3, 4, 5)
        check('20140203 040', ValueError)
        check('20140203 04', 2014, 2, 3, 4)


if __name__ == '__main__':
    unittest.main()
