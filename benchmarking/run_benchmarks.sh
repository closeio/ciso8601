tox -- '2014-01-09T21:48:00'
tox -- '2014-01-09T21:48:00-05:30'
python format_results.py benchmark_results/2014-01-09T214800 benchmark_results/benchmark_with_no_time_zone.rst
python format_results.py benchmark_results/2014-01-09T214800-0530 benchmark_results/benchmark_with_time_zone.rst
python rst_include_replace.py ../README.rst 'benchmark_with_no_time_zone.rst' benchmark_results/benchmark_with_no_time_zone.rst
python rst_include_replace.py ../README.rst 'benchmark_with_time_zone.rst' benchmark_results/benchmark_with_time_zone.rst
python rst_include_replace.py ../README.rst 'benchmark_module_versions.rst' benchmark_results/benchmark_module_versions.rst
