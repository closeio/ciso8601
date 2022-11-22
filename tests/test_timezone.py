# -*- coding: utf-8 -*-

import sys
import unittest

from datetime import datetime, timedelta

from ciso8601 import FixedOffset

if sys.version_info.major == 2:
    # We use add `unittest.TestCase.assertRaisesRegex` method, which is called `assertRaisesRegexp` in Python 2.
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp

class TimezoneTestCase(unittest.TestCase):
    def test_utcoffset(self):
        if sys.version_info >= (3, 2):
            from datetime import timezone
            for minutes in range(-1439, 1440):
                td = timedelta(minutes=minutes)
                tz = timezone(td)
                built_in_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=tz)
                our_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=FixedOffset(minutes * 60))
                self.assertEqual(built_in_dt.utcoffset(), our_dt.utcoffset(), "`utcoffset` output did not match for offset: {minutes}".format(minutes=minutes))
                self.assertEqual(built_in_dt.tzinfo.utcoffset(built_in_dt), our_dt.tzinfo.utcoffset(our_dt), "`tzinfo.utcoffset` output did not match for offset: {minutes}".format(minutes=minutes))
        else:
            for seconds in [0, +0, -0, -4980, +45240]:
                offset = FixedOffset(seconds)
                our_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=offset)
                self.assertEqual(our_dt.utcoffset(), timedelta(seconds=seconds))
                self.assertEqual(offset.utcoffset(our_dt), timedelta(seconds=seconds))

    def test_dst(self):
        if sys.version_info >= (3, 2):
            from datetime import timezone
            for minutes in range(-1439, 1440):
                td = timedelta(minutes=minutes)
                tz = timezone(td)
                built_in_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=tz)
                our_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=FixedOffset(minutes * 60))
                self.assertEqual(built_in_dt.dst(), our_dt.dst(), "`dst` output did not match for offset: {minutes}".format(minutes=minutes))
                self.assertEqual(built_in_dt.tzinfo.dst(built_in_dt), our_dt.tzinfo.dst(our_dt), "`tzinfo.dst` output did not match for offset: {minutes}".format(minutes=minutes))
        else:
            for seconds in [0, +0, -0, -4980, +45240]:
                offset = FixedOffset(seconds)
                our_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=offset)
                self.assertIsNone(our_dt.dst())
                self.assertIsNone(offset.dst(our_dt))

    def test_tzname(self):
        if sys.version_info >= (3, 2):
            from datetime import timezone
            for minutes in range(-1439, 1440):
                td = timedelta(minutes=minutes)
                tz = timezone(td)
                built_in_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=tz)
                our_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=FixedOffset(minutes * 60))
                self.assertEqual(built_in_dt.tzname(), our_dt.tzname(), "`tzname` output did not match for offset: {minutes}".format(minutes=minutes))
                self.assertEqual(built_in_dt.tzinfo.tzname(built_in_dt), our_dt.tzinfo.tzname(our_dt), "`tzinfo.tzname` output did not match for offset: {minutes}".format(minutes=minutes))
        else:
            for seconds, expected_tzname in [(0, "UTC+00:00"), (+0, "UTC+00:00"), (-0, "UTC+00:00"), (-4980, "UTC-01:23"), (+45240, "UTC+12:34")]:
                offset = FixedOffset(seconds)
                our_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=offset)
                self.assertEqual(our_dt.tzname(), expected_tzname)
                self.assertEqual(offset.tzname(our_dt), expected_tzname)

    def test_fromutc(self):
        # https://github.com/closeio/ciso8601/issues/108
        our_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=FixedOffset(60 * 60))
        expected_dt = datetime(2014, 2, 3, 11, 35, 27, 234567, tzinfo=FixedOffset(60 * 60))
        self.assertEqual(expected_dt, our_dt.tzinfo.fromutc(our_dt))

        if sys.version_info >= (3, 2):
            from datetime import timezone
            td = timedelta(minutes=60)
            tz = timezone(td)
            built_in_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=tz)
            built_in_result = built_in_dt.tzinfo.fromutc(built_in_dt)
            self.assertEqual(expected_dt, built_in_result)

    def test_fromutc_straddling_a_day_boundary(self):
        our_dt = datetime(2020, 2, 29, 23, 35, 27, 234567, tzinfo=FixedOffset(60 * 60))
        expected_dt = datetime(2020, 3, 1, 0, 35, 27, 234567, tzinfo=FixedOffset(60 * 60))
        self.assertEqual(expected_dt, our_dt.tzinfo.fromutc(our_dt))

    def test_fromutc_fails_if_given_non_datetime(self):
        our_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=FixedOffset(60 * 60))
        with self.assertRaises(TypeError, msg="fromutc: argument must be a datetime"):
            our_dt.tzinfo.fromutc(123)

    def test_fromutc_fails_if_tzinfo_is_none(self):
        our_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=FixedOffset(60 * 60))
        other_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=None)
        with self.assertRaises(ValueError, msg="fromutc: dt.tzinfo is not self"):
            our_dt.tzinfo.fromutc(other_dt)

    def test_fromutc_fails_if_tzinfo_is_some_other_offset(self):
        our_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=FixedOffset(60 * 60))
        other_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=FixedOffset(120 * 60))
        with self.assertRaises(ValueError, msg="fromutc: dt.tzinfo is not self"):
            our_dt.tzinfo.fromutc(other_dt)

if __name__ == '__main__':
    unittest.main()
