import argparse
import csv
import os
import platform
import pytablewriter
import re

from collections import defaultdict, UserDict


class Result:
    def __init__(self, timing, parsed_value, exception, matched_expected):
        self.timing = timing
        self.parsed_value = parsed_value
        self.exception = exception
        self.matched_expected = matched_expected

    def formatted_timing(self):
        return format_duration(self.timing) if self.timing is not None else ""

    def __str__(self):
        if self.exception:
            return f"Raised  ``{self.exception}`` Exception"
        elif not self.matched_expected:
            return f"**Incorrect Result** (``{self.parsed_value}``)"
        else:
            return self.formatted_timing()


class ModuleResults(UserDict):
    def most_modern_result(self):
        non_exception_results = [(_python_version, result) for _python_version, result in self.data.items() if result.exception is None]
        return sorted(non_exception_results, key=lambda kvp: kvp[0], reverse=True)[0][1]

FILENAME_REGEX_RAW = r"benchmark_timings_python(\d)(\d).csv"
FILENAME_REGEX = re.compile(FILENAME_REGEX_RAW)

MODULE_VERSION_FILENAME_REGEX_RAW = r"module_versions_python(\d)(\d).csv"
MODULE_VERSION_FILENAME_REGEX = re.compile(MODULE_VERSION_FILENAME_REGEX_RAW)

UNITS = {"nsec": 1e-9, "usec": 1e-6, "msec": 1e-3, "sec": 1.0}
SCALES = sorted([(scale, unit) for unit, scale in UNITS.items()], reverse=True)

NOT_APPLICABLE = 'N/A'


def format_duration(duration):
    # Based on cPython's `timeit` CLI formatting
    scale, unit = next(((scale, unit) for scale, unit in SCALES if duration >= scale), SCALES[-1])
    precision = 3
    return "%.*g %s" % (precision, duration / scale, unit)


def format_relative(d1, d2):
    if d1 is None or d2 is None:
        return NOT_APPLICABLE
    precision = 1
    return "%.*fx" % (precision, d1 / d2)


def format_used_module_versions(module_versions_used):
    results = []
    for module, versions in sorted(module_versions_used.items(), key=lambda x: x[0].lower()):
        if len(versions) == 1:
            results.append(f"{module}=={next(iter(versions.keys()))}")
        else:
            results.append(", ".join([f"{module}=={version} (on Python {', '.join(sorted(py_versions))})" for version, py_versions in versions.items()]))
    return results


def relative_slowdown(subject, comparison):
    most_modern_common_version = next(iter(sorted(set(subject.keys()).intersection(set(comparison)), reverse=True)), None)

    if not most_modern_common_version:
        raise ValueError("No common Python version found")

    return format_relative(subject[most_modern_common_version].timing, comparison[most_modern_common_version].timing)


def filepaths(directory, condition):
    return [os.path.join(parent, f) for parent, _dirs, files in os.walk(directory) for f in files if condition(f)]

def load_benchmarking_results(results_directory):
    calling_code = {}
    timestamps = set()
    python_versions = set()
    results = defaultdict(ModuleResults)

    files_to_process = filepaths(results_directory, FILENAME_REGEX.match)
    for csv_file in files_to_process:
        try:
            with open(csv_file, "r") as fin:
                reader = csv.reader(fin, delimiter=",", quotechar='"')
                major, minor, timestamp = next(reader)
                timestamps.add(timestamp)
                for module, _setup, stmt, parse_result, count, time_taken, matched, exception in reader:
                    timing = float(time_taken) / int(count) if exception == "" else None
                    exception = exception if exception != "" else None
                    results[module][(major, minor)] = Result(
                        timing,
                        parse_result,
                        exception,
                        matched == "True"
                    )
                    python_versions.add((major, minor))
                    calling_code[module] = f"``{stmt.format(timestamp=timestamp)}``"
        except Exception:
            print(f"Problem while parsing `{csv_file}`")
            raise

    if len(timestamps) > 1:
        raise NotImplementedError(f"Found a mix of files in the results directory. Found files that represent the parsing of {timestamps}. Support for handling multiple timestamps is not implemented.")

    python_versions_by_modernity = sorted(python_versions, reverse=True)
    return results, python_versions_by_modernity, calling_code


def write_benchmarking_results(results_directory, output_file, baseline_module, include_call):
    results, python_versions_by_modernity, calling_code = load_benchmarking_results(results_directory)
    modules_by_modern_speed = [module for module, results in sorted([*results.items()], key=lambda kvp: kvp[1].most_modern_result().timing)]

    writer = pytablewriter.RstGridTableWriter()
    formatted_python_versions = ["Python {}".format(".".join(key)) for key in python_versions_by_modernity]
    writer.header_list = ["Module"] + (["Call"] if include_call else []) + formatted_python_versions + [f"Relative Slowdown (versus {baseline_module}, latest Python)"]
    writer.type_hint_list = [pytablewriter.String] * len(writer.header_list)

    calling_codes = [calling_code[module] for module in modules_by_modern_speed]
    performance_results = [[results[module].get(python_version, NOT_APPLICABLE) for python_version in python_versions_by_modernity] for module in modules_by_modern_speed]
    relative_slowdowns = [relative_slowdown(results[module], results[baseline_module]) if module != baseline_module else NOT_APPLICABLE for module in modules_by_modern_speed]

    writer.value_matrix = [
        [module] + ([calling_code[module]] if include_call else []) + performance_by_version + [relative_slowdown] for module, calling_code, performance_by_version, relative_slowdown in zip(modules_by_modern_speed, calling_codes, performance_results, relative_slowdowns)
    ]

    with open(output_file, 'w') as fout:
        writer.stream = fout
        writer.write_table()
        fout.write('\n')

        if len(modules_by_modern_speed) > 1:
            baseline_module_timing = results[baseline_module].most_modern_result().formatted_timing()

            fastest_module, next_fastest_module = modules_by_modern_speed[0:2]
            if fastest_module == baseline_module:
                fout.write(f"{baseline_module} takes {baseline_module_timing}, which is **{relative_slowdown(results[next_fastest_module], results[baseline_module])} faster than {next_fastest_module}**, the next fastest ISO 8601 parser in this comparison.\n")
            else:
                fout.write(f"{baseline_module} takes {baseline_module_timing}, which is **{relative_slowdown(results[baseline_module], results[fastest_module])} slower than {fastest_module}**, the fastest ISO 8601 parser in this comparison.\n")


def load_module_version_info(results_directory):
    module_versions_used = defaultdict(dict)
    files_to_process = filepaths(results_directory, MODULE_VERSION_FILENAME_REGEX.match)
    for csv_file in files_to_process:
        with open(csv_file, "r") as fin:
            reader = csv.reader(fin, delimiter=",", quotechar='"')
            major, minor = next(reader)
            for module, version in reader:
                if version not in module_versions_used[module]:
                    module_versions_used[module][version] = set()
                module_versions_used[module][version].add(".".join((major, minor)))
    return module_versions_used


def write_module_version_info(results_directory, output_file):
    with open(output_file, 'w') as fout:
        fout.write(f"Tested on {platform.system()} {platform.release()} using the following modules:\n")
        fout.write('\n')
        fout.write(".. code:: python\n")
        fout.write('\n')
        for module_version_line in format_used_module_versions(load_module_version_info(results_directory)):
            fout.write(f"  {module_version_line}\n")


def main(results_directory, output_file, baseline_module, include_call, module_version_output):
    write_benchmarking_results(results_directory, output_file, baseline_module, include_call)
    write_module_version_info(results_directory, os.path.join(os.path.dirname(output_file), module_version_output))


if __name__ == '__main__':
    OUTPUT_FILE_HELP = "The filepath to use when outputting the reStructuredText results."
    RESULTS_DIR_HELP = f"Which directory the script should look in to find benchmarking results. Will process any file that match the regexes '{FILENAME_REGEX_RAW}' and '{MODULE_VERSION_FILENAME_REGEX_RAW}'."

    BASELINE_LIBRARY_DEFAULT = "ciso8601"
    BASELINE_LIBRARY_HELP = f"The module to make all relative calculations relative to (default: \"{BASELINE_LIBRARY_DEFAULT}\")."

    INCLUDE_CALL_DEFAULT = False
    INCLUDE_CALL_HELP = f"Whether or not to include a column showing the actual code call (default: {INCLUDE_CALL_DEFAULT})."

    MODULE_VERSION_OUTPUT_FILE_DEFAULT = "benchmark_module_versions.rst"
    MODULE_VERSION_OUTPUT_FILE_HELP = "The filename to use when outputting the reStructuredText list of module versions. Written to the same directory as `OUTPUT`"

    parser = argparse.ArgumentParser("Formats the benchmarking results into a nicely formatted block of reStructuredText for use in the README.")
    parser.add_argument("RESULTS", help=RESULTS_DIR_HELP)
    parser.add_argument("OUTPUT", help=OUTPUT_FILE_HELP)
    parser.add_argument("--baseline-module", required=False, default=BASELINE_LIBRARY_DEFAULT, help=BASELINE_LIBRARY_HELP)
    parser.add_argument("--include-call", required=False, type=bool, default=INCLUDE_CALL_DEFAULT, help=INCLUDE_CALL_HELP)
    parser.add_argument("--module-version-output", required=False, default=MODULE_VERSION_OUTPUT_FILE_DEFAULT, help=MODULE_VERSION_OUTPUT_FILE_HELP)

    args = parser.parse_args()

    if not os.path.exists(args.RESULTS):
        raise ValueError(f'Results directory "{args.RESULTS}" does not exist.')

    main(args.RESULTS, args.OUTPUT, args.baseline_module, args.include_call, args.module_version_output)
