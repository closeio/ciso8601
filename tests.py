import ciso8601
import datetime
import pytz
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
                ciso8601.parse_datetime_unaware('{}-02-29'.format(leap_year)),
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

    def test_unaware(self):
        expected = datetime.datetime(2014, 12, 5, 12, 30, 45, 123456)
        self.assertEqual(
            ciso8601.parse_datetime('2014-12-05T12:30:45.123456'),
            expected
        )

        # parse_datetime_unaware ignores tz offset
        self.assertEqual(
            ciso8601.parse_datetime_unaware('2014-12-05T12:30:45.123456Z'),
            expected
        )
        self.assertEqual(
            ciso8601.parse_datetime_unaware('2014-12-05T12:30:45.123456+00:00'),
            expected,
        )
        self.assertEqual(
            ciso8601.parse_datetime_unaware('2014-12-05T12:30:45.123456-05:00'),
            expected,
        )

    def test_invalid(self):
        self.assertRaises(
            ValueError,
            ciso8601.parse_datetime_unaware,
            'asdf',
        )
        self.assertRaises(
            ValueError,
            ciso8601.parse_datetime_unaware,
            '2014-99-03',
        )
        self.assertRaises(
            ValueError,
            ciso8601.parse_datetime_unaware,
            '2014-13-03',
        )
        self.assertRaises(
            ValueError,
            ciso8601.parse_datetime_unaware,
            '2014-00-03',
        )
        self.assertRaises(
            ValueError,
            ciso8601.parse_datetime,
            '20140203T24:35:27',
        )
        self.assertRaises(
            ValueError,
            ciso8601.parse_datetime,
            '20140203T23:60:27',
        )
        self.assertRaises(
            ValueError,
            ciso8601.parse_datetime,
            '20140203T23:35:61',
        )
        self.assertRaises(
            ValueError,
            ciso8601.parse_datetime_unaware,
            '2014-01-32',
        )
        self.assertRaises(
            ValueError,
            ciso8601.parse_datetime_unaware,
            '2014-06-31',
        )
        for non_leap_year in (1700, 1800, 1900, 2014):
            self.assertRaises(
                ValueError,
                ciso8601.parse_datetime_unaware,
                '{}-02-29'.format(non_leap_year)
            )
        self.assertRaises(
            ValueError,
            ciso8601.parse_datetime_unaware,
            'Z',
        )

        self.assertRaises(
            ValueError,
            ciso8601.parse_datetime,
            '2014-12-05asdfasdf'
        )

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
        check('20140203 04:05:0.123', None)
        check('20140203 04:05:.123', None)
        check('20140203 04:05:,123', None)
        check('20140203 04:05:06.', 2014, 2, 3, 4, 5, 6)
        check('20140203 0405:06.', 2014, 2, 3, 4, 5, 6)
        check('20140203 040506.', 2014, 2, 3, 4, 5, 6)
        check('20140203 04050.', None)
        check('20140203 0405:0', None)
        check('20140203 04:05:.', None)
        check('20140203 04:05:,', None)
        check('20140203 04::', None)
        check('20140203 04:00:', 2014, 2, 3, 4)
        check('20140203 04::01', None)
        check('20140203 04:', 2014, 2, 3, 4)

        check('2014-02-03', 2014, 2, 3)
        check('2014-0-03', None)
        check('2014--03', None)
        check('2014-02', 2014, 2, 1)
        check('2014--0', None)
        check('2014--', None)
        check('2014-', None)
        check('2014', None)

        check('20140203 040506.123', 2014, 2, 3, 4, 5, 6, 123000)
        check('20140203 040506123', 2014, 2, 3, 4, 5, 6)  # NB: drops usec
        check('20140203 04050612', 2014, 2, 3, 4, 5, 6)
        check('20140203 0405061', 2014, 2, 3, 4, 5, 6)
        check('20140203 040506', 2014, 2, 3, 4, 5, 6)
        check('20140203 04050', None)
        check('20140203 0405', 2014, 2, 3, 4, 5)
        check('20140203 040', None)
        check('20140203 04', 2014, 2, 3, 4)

if __name__ == '__main__':
    unittest.main()
