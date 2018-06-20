# -*- coding: utf-8 -*-

import sys

from datetime import datetime, timedelta

from ciso8601 import FixedOffset

if sys.version_info.major == 2:
    # We use unittest2 since it has a backport of the `unittest.TestCase.assertRaisesRegex` method,
    # which is called `assertRaisesRegexp` in Python 2. This saves us the hassle of monkey-patching
    # the class ourselves.
    import unittest2 as unittest
else:
    import unittest


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
        else:
            self.assertEqual(FixedOffset(0).utcoffset(), timedelta(minutes=0))
            self.assertEqual(FixedOffset(+0).utcoffset(), timedelta(minutes=0))
            self.assertEqual(FixedOffset(-0).utcoffset(), timedelta(minutes=0))
            self.assertEqual(FixedOffset(-4980).utcoffset(), timedelta(hours=-1, minutes=-23))
            self.assertEqual(FixedOffset(+45240).utcoffset(), timedelta(hours=12, minutes=34))

    def test_dst(self):
        if sys.version_info >= (3, 2):
            from datetime import timezone
            for minutes in range(-1439, 1440):
                td = timedelta(minutes=minutes)
                tz = timezone(td)
                built_in_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=tz)
                our_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=FixedOffset(minutes * 60))
                self.assertEqual(built_in_dt.dst(), our_dt.dst(), "`dst` output did not match for offset: {minutes}".format(minutes=minutes))
        else:
            self.assertIsNone(FixedOffset(0).dst(), "UTC")
            self.assertIsNone(FixedOffset(+0).dst(), "UTC")
            self.assertIsNone(FixedOffset(-0).dst(), "UTC")
            self.assertIsNone(FixedOffset(-4980).dst(), "UTC-01:23")
            self.assertIsNone(FixedOffset(+45240).dst(), "UTC+12:34")

    def test_tzname(self):
        if sys.version_info >= (3, 2):
            from datetime import timezone
            for minutes in range(-1439, 1440):
                td = timedelta(minutes=minutes)
                tz = timezone(td)
                built_in_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=tz)
                our_dt = datetime(2014, 2, 3, 10, 35, 27, 234567, tzinfo=FixedOffset(minutes * 60))
                self.assertEqual(built_in_dt.tzname(), our_dt.tzname(), "`tzname` output did not match for offset: {minutes}".format(minutes=minutes))
        else:
            self.assertEqual(FixedOffset(0).tzname(), "UTC+00:00")
            self.assertEqual(FixedOffset(+0).tzname(), "UTC+00:00")
            self.assertEqual(FixedOffset(-0).tzname(), "UTC+00:00")
            self.assertEqual(FixedOffset(-4980).tzname(), "UTC-01:23")
            self.assertEqual(FixedOffset(+45240).tzname(), "UTC+12:34")

if __name__ == '__main__':
    unittest.main()
