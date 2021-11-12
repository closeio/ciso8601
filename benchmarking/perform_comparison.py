import argparse
import csv
import os
import sys
import timeit

from datetime import datetime, timedelta

import pytz

if (sys.version_info.major, sys.version_info.minor) >= (3, 5):
    from metomi.isodatetime.data import TimePoint

try:
    from importlib.metadata import version as get_module_version
except ImportError:
    from importlib_metadata import version as get_module_version

ISO_8601_MODULES = {
    "aniso8601": ("import aniso8601", "aniso8601.parse_datetime('{timestamp}')"),
    "ciso8601": ("import ciso8601", "ciso8601.parse_datetime('{timestamp}')"),
    "python-dateutil": ("import dateutil.parser", "dateutil.parser.parse('{timestamp}')"),
    "iso8601": ("import iso8601", "iso8601.parse_date('{timestamp}')"),
    "isodate": ("import isodate", "isodate.parse_datetime('{timestamp}')"),
    "maya": ("import maya", "maya.parse('{timestamp}').datetime()"),
    "pendulum": ("from pendulum.parsing import parse_iso8601", "parse_iso8601('{timestamp}')"),
    "PySO8601": ("import PySO8601", "PySO8601.parse('{timestamp}')"),
    "str2date": ("from str2date import str2date", "str2date('{timestamp}')"),
}

if os.name != "nt" and (sys.version_info.major, sys.version_info.minor) < (3, 9):
    # udatetime doesn't support Windows.
    ISO_8601_MODULES["udatetime"] = ("import udatetime", "udatetime.from_string('{timestamp}')")

if (sys.version_info.major, sys.version_info.minor) >= (3, 5):
    # metomi-isodatetime doesn't support Python < 3.5
    ISO_8601_MODULES["metomi-isodatetime"] = ("import metomi.isodatetime.parsers as parse", "parse.TimePointParser().parse('{timestamp}')")

if (sys.version_info.major, sys.version_info.minor) >= (3, 6):
    # zulu v2.0.0+ no longer supports Python < 3.6
    ISO_8601_MODULES["zulu"] = ("import zulu", "zulu.parse('{timestamp}')")

if (sys.version_info.major, sys.version_info.minor) != (3, 6) and (sys.version_info.major, sys.version_info.minor) != (3, 10):
    # iso8601utils installs enum34, which messes with tox in Python 3.6
    # https://stackoverflow.com/q/43124775
    # https://github.com/silverfernsys/iso8601utils/pull/5
    # iso8601utils uses `from collections import Iterable` which no longer works in Python 3.10
    # https://github.com/silverfernsys/iso8601utils/issues/6
    ISO_8601_MODULES["iso8601utils"] = ("from iso8601utils import parsers", "parsers.datetime('{timestamp}')")

if (sys.version_info.major, sys.version_info.minor) != (3, 4):
    # arrow no longer supports Python 3.4
    ISO_8601_MODULES["arrow"] = ("import arrow", "arrow.get('{timestamp}').datetime")
    # moment is built on `times`, which is built on `arrow`, which no longer supports Python 3.4
    ISO_8601_MODULES["moment"] = ("import moment", "moment.date('{timestamp}').date")

class Result:
    def __init__(self, module, setup, stmt, parse_result, count, time_taken, matched, exception):
        self.module = module
        self.setup = setup
        self.stmt = stmt
        self.parse_result = parse_result
        self.count = count
        self.time_taken = time_taken
        self.matched = matched
        self.exception = exception

    def to_row(self):
        return [
            self.module,
            self.setup,
            self.stmt,
            self.parse_result,
            self.count,
            self.time_taken,
            self.matched,
            self.exception
        ]

def metomi_compare(timepoint, dt):
    # Really (s)crappy comparison function
    # Ignores subsecond accuracy.
    # https://github.com/metomi/isodatetime/issues/196
    offset = timedelta(hours=timepoint.time_zone.hours, minutes=timepoint.time_zone.minutes)
    return timepoint.year == dt.year and \
        timepoint.month_of_year == dt.month and \
        timepoint.day_of_month == dt.day and \
        timepoint.hour_of_day == dt.hour and \
        timepoint.minute_of_hour == dt.minute and \
        timepoint.second_of_minute == dt.second and \
        offset == dt.tzinfo.utcoffset(dt)

def check_roughly_equivalent(dt1, dt2):
    # For the purposes of our benchmarking, we don't care if the datetime
    # has tzinfo=UTC or is naive.
    dt1 = dt1.replace(tzinfo=pytz.UTC) if isinstance(dt1, datetime) and dt1.tzinfo is None else dt1
    dt2 = dt2.replace(tzinfo=pytz.UTC) if isinstance(dt2, datetime) and dt2.tzinfo is None else dt2

    # Special handling for metomi-isodatetime
    if (sys.version_info.major, sys.version_info.minor) >= (3, 5) and isinstance(dt1, TimePoint):
        return metomi_compare(dt1, dt2)

    return dt1 == dt2

def auto_range_counts(filepath):
    results = {}
    if os.path.exists(filepath):
        with open(filepath, "r") as fin:
            reader = csv.reader(fin, delimiter=",", quotechar='"')
            for module, count in reader:
                results[module] = int(count)
    return results

def update_auto_range_counts(filepath, results):
    new_counts = dict([[result.module, result.count] for result in results if result.count is not None])
    new_auto_range_counts = auto_range_counts(filepath)
    new_auto_range_counts.update(new_counts)
    with open(filepath, "w") as fout:
        auto_range_file_writer = csv.writer(fout, delimiter=",", quotechar='"', lineterminator="\n")
        for module, count in sorted(new_auto_range_counts.items()):
            auto_range_file_writer.writerow([module, count])

def write_results(filepath, timestamp, results):
    with open(filepath, "w") as fout:
        writer = csv.writer(fout, delimiter=",", quotechar='"', lineterminator="\n")
        writer.writerow([sys.version_info.major, sys.version_info.minor, timestamp])
        for result in results:
            writer.writerow(result.to_row())

def write_module_versions(filepath):
    with open(filepath, "w") as fout:
        module_version_writer = csv.writer(fout, delimiter=",", quotechar='"', lineterminator="\n")
        module_version_writer.writerow([sys.version_info.major, sys.version_info.minor])
        for module, (_setup, _stmt) in sorted(ISO_8601_MODULES.items(), key=lambda x: x[0].lower()):
            module_version_writer.writerow([module, get_module_version(module)])

def run_tests(timestamp, results_directory, compare_to):
    # `Timer.autorange` only exists in Python 3.6+. We want the tests to run in a reasonable amount of time,
    # but we don't want to have to hard-code how many times to run each test.
    # So we make sure to call Python 3.6+ versions first. They output a file that the others use to know how many iterations to run.
    auto_range_count_filepath = os.path.join(results_directory, "auto_range_counts.csv")
    test_interation_counts = auto_range_counts(auto_range_count_filepath)

    exec(ISO_8601_MODULES[compare_to][0])
    expected_parse_result = eval(ISO_8601_MODULES[compare_to][1].format(timestamp=timestamp))

    results = []

    for module, (setup, stmt) in ISO_8601_MODULES.items():
        count = None
        time_taken = None
        exception = None
        try:
            exec(setup)
            parse_result = eval(stmt.format(timestamp=timestamp))

            timer = timeit.Timer(stmt=stmt.format(timestamp=timestamp), setup=setup)
            if hasattr(timer, 'autorange'):
                count, time_taken = timer.autorange()
            else:
                count = test_interation_counts[module]
                time_taken = timer.timeit(number=count)
        except Exception as exc:
            count = None
            time_taken = None
            parse_result = None
            exception = type(exc)

        results.append(
            Result(
                module,
                setup,
                stmt.format(timestamp=timestamp),
                parse_result if parse_result is not None else "None",
                count,
                time_taken,
                check_roughly_equivalent(parse_result, expected_parse_result),
                exception,
            )
        )

    update_auto_range_counts(auto_range_count_filepath, results)

    results_filepath = os.path.join(results_directory, "benchmark_timings_python{major}{minor}.csv".format(major=sys.version_info.major, minor=sys.version_info.minor))
    write_results(results_filepath, timestamp, results)

    module_versions_filepath = os.path.join(results_directory, "module_versions_python{major}{minor}.csv".format(major=sys.version_info.major, minor=sys.version_info.minor))
    write_module_versions(module_versions_filepath)

def sanitize_timestamp_as_filename(timestamp):
    return timestamp.replace(":", "")

if __name__ == "__main__":
    TIMESTAMP_HELP = "Which ISO 8601 timestamp to parse"

    BASE_LIBRARY_DEFAULT = "ciso8601"
    BASE_LIBRARY_HELP = 'The module to make correctness decisions relative to (default: "{default}").'.format(default=BASE_LIBRARY_DEFAULT)

    RESULTS_DIR_DEFAULT = "benchmark_results"
    RESULTS_DIR_HELP = 'Which directory the script should output benchmarking results. (default: "{0}")'.format(RESULTS_DIR_DEFAULT)

    parser = argparse.ArgumentParser("Runs `timeit` to benchmark a variety of ISO 8601 parsers.")
    parser.add_argument("TIMESTAMP", help=TIMESTAMP_HELP)
    parser.add_argument("--base-module", required=False, default=BASE_LIBRARY_DEFAULT, help=BASE_LIBRARY_HELP)
    parser.add_argument("--results", required=False, default=RESULTS_DIR_DEFAULT, help=RESULTS_DIR_HELP)
    args = parser.parse_args()

    output_dir = os.path.join(args.results, sanitize_timestamp_as_filename(args.TIMESTAMP))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    run_tests(args.TIMESTAMP, output_dir, args.base_module)
