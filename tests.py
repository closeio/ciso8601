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
        self.assertEqual(
            ciso8601.parse_datetime_unaware('asdf'),
            None,
        )
        self.assertEqual(
            ciso8601.parse_datetime_unaware('2014-99-03'),
            None,
        )
        self.assertEqual(
            ciso8601.parse_datetime_unaware('2014-13-03'),
            None,
        )
        self.assertEqual(
            ciso8601.parse_datetime('20140203T24:35:27'),
            None,
        )
        self.assertEqual(
            ciso8601.parse_datetime('20140203T23:60:27'),
            None,
        )
        self.assertEqual(
            ciso8601.parse_datetime('20140203T23:35:61'),
            None,
        )
        self.assertEqual(
            ciso8601.parse_datetime_unaware('2014-01-32'),
            None,
        )
        self.assertEqual(
            ciso8601.parse_datetime_unaware('2014-06-31'),
            None,
        )
        for non_leap_year in (1700, 1800, 1900, 2014):
            self.assertEqual(
                ciso8601.parse_datetime_unaware('{}-02-29'.format(non_leap_year)),
                None,
            )
        self.assertEqual(
            ciso8601.parse_datetime_unaware('Z'),
            None,
        )
        self.assertEqual(
            ciso8601.parse_datetime('2014-12-05asdfasdf'),
            datetime.datetime(2014, 12, 5)
        )

if __name__ == '__main__':
    unittest.main()
