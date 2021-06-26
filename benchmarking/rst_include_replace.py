import argparse
import os
import re

# Since GitHub doesn't support the use of the reStructuredText `include` directive,
# we must copy-paste the results into README.rst. To do this automatically, we came
# up with a special comment syntax. This script will replace everything between the
# two special comments with the content requested.
# For example:
#
# .. <include:benchmark_module_versions.rst>
# This content will be replaced by the content of "benchmark_module_versions.rst"
# .. </include:benchmark_module_versions.rst>
#
INCLUDE_BLOCK_START = ".. <include:{filename}>"
INCLUDE_BLOCK_END = ".. </include:{filename}>"


def replace_include(target_filepath, include_file, source_filepath):
    start_block_regex = re.compile(INCLUDE_BLOCK_START.format(filename=include_file))
    end_block_regex = re.compile(INCLUDE_BLOCK_END.format(filename=include_file))

    with open(source_filepath, "r") as fin:
        replacement_lines = iter(fin.readlines())

    with open(target_filepath, "r") as fin:
        target_lines = iter(fin.readlines())
    with open(target_filepath, "w") as fout:
        for line in target_lines:
            if start_block_regex.match(line):
                fout.write(line)
                fout.write("\n")  # rST requires a blank line after comment lines
                for replacement_line in replacement_lines:
                    fout.write(replacement_line)
                next_line = next(target_lines)
                while not end_block_regex.match(next_line):
                    try:
                        next_line = next(target_lines)
                    except StopIteration:
                        break
                fout.write("\n")  # rST requires a blank line before comment lines
                fout.write(next_line)
            else:
                fout.write(line)


if __name__ == "__main__":
    TARGET_HELP = "The filepath you wish to replace tags within."
    INCLUDE_TAG_HELP = "The filename within the tag you are hoping to replace. (ex. 'benchmark_with_time_zone.rst')"
    SOURCE_HELP = "The filepath whose contents should be included into the TARGET file."

    parser = argparse.ArgumentParser("Formats the benchmarking results into a nicely formatted block of reStructuredText for use in the README.")
    parser.add_argument("TARGET", help=TARGET_HELP)
    parser.add_argument("INCLUDE_TAG", help=INCLUDE_TAG_HELP)
    parser.add_argument("SOURCE", help=SOURCE_HELP)

    args = parser.parse_args()

    if not os.path.exists(args.TARGET):
        raise ValueError(f"TARGET path {args.TARGET} does not exist")

    if not os.path.exists(args.SOURCE):
        raise ValueError(f"SOURCE path {args.SOURCE} does not exist")

    replace_include(args.TARGET, args.INCLUDE_TAG, args.SOURCE)
