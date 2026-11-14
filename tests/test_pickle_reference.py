import gc
import pickle
import sys
import unittest

from ciso8601 import FixedOffset


class FixedOffsetPickleRefcountTests(unittest.TestCase):
    @unittest.skipUnless(sys.implementation.name == "cpython", "CPython reference counts")
    def test_getinitargs_owns_only_tuple_reference(self):
        for seconds in (-86399, -3600, 3600, 86399):
            with self.subTest(seconds=seconds):
                offset = FixedOffset(seconds)
                args = offset.__getinitargs__()
                values = [args[0]]
                controls = [int(str(seconds))]
                del args
                gc.collect()
                # Compare equivalent live references instead of assuming a
                # particular interpreter's temporary-argument refcount.
                self.assertEqual(values, controls)
                self.assertEqual(
                    sys.getrefcount(values[0]), sys.getrefcount(controls[0])
                )

    def test_fixed_offset_pickle_roundtrip(self):
        for seconds in (-86399, -3600, 0, 3600, 86399):
            for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
                with self.subTest(seconds=seconds, protocol=protocol):
                    offset = FixedOffset(seconds)
                    result = pickle.loads(pickle.dumps(offset, protocol=protocol))
                    self.assertEqual(result.utcoffset(None), offset.utcoffset(None))
                    self.assertEqual(result.tzname(None), offset.tzname(None))


if __name__ == "__main__":
    unittest.main()
