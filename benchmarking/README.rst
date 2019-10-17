=====================
Benchmarking ciso8601
=====================

.. contents:: Contents

Introduction
------------

``ciso8601``'s goal is to be the world's fastest ISO 8601 datetime parser for Python (**Note:** ciso8601 `only supports a subset of ISO 8601`_).

.. _`only supports a subset of ISO 8601`: https://github.com/closeio/ciso8601#supported-subset-of-iso-8601

In order to see how we compare, we run benchmarks against each other known ISO 8601 parser.

**Note:** We only run benchmarks against open-source parsers that are published as part of Python modules on `PyPI`_.

.. _`PyPI`: https://pypi.org/

Quick start: Running the standard benchmarks
--------------------------------------------

If you just want to run the standard benchmarks we run for each release, there is a convenience script.

.. code:: bash

  % python -m venv env
  % source env/bin/activate
  % pip install -r requirements.txt
  % ./run_benchmarks.sh

This runs the benchmarks and generates reStructuredText files. The contents of these files are then automatically copy-pasted into ciso8601's `README.rst`_.

.. _`README.rst`: https://github.com/closeio/ciso8601/blob/master/README.rst

Running custom benchmarks
-------------------------

Running a custom benchmark is done by supplying `tox`_ with your custom timestamp: 

.. code:: bash

  % python -m venv env
  % source env/bin/activate
  % pip install -r requirements.txt
  % tox '2014-01-09T21:48:00'

It calls `perform_comparison.py`_ in each of the supported Python interpreters on your machine.
This in turn calls `timeit`_ for each of the modules defined in ``ISO_8601_MODULES``. 

.. _`tox`: https://tox.readthedocs.io/en/latest/index.html
.. _`timeit`: https://docs.python.org/3/library/timeit.html

Results are dumped into a collection of CSV files (in the ``benchmark_results`` directory by default).

These CSV files can then formatted into reStructuredText tables by `format_results.py`_:

.. _`perform_comparison.py`: https://github.com/closeio/ciso8601/blob/master/benchmarking/perform_comparison.py
.. _`format_results.py`: https://github.com/closeio/ciso8601/blob/master/benchmarking/format_results.py

.. code:: bash

  % cd benchmarking
  % python format_results.py benchmark_results/2014-01-09T214800 benchmark_results/benchmark_with_no_time_zone.rst
  % python format_results.py benchmark_results/2014-01-09T214800-0530 benchmark_results/benchmark_with_time_zone.rst

Disclaimer
-----------

Because of the way that ``tox`` works (and the way the benchmark is structured more generally), it doesn't make sense to compare the results for a given module across different Python versions.
Comparisons between modules within the same Python version are still valid, and indeed, are the goal of the benchmarks.

FAQs
----

"What about <missing module>?"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We only run benchmarks against open-source parsers that are published as part of Python modules on PyPI.

Do you know of a competing module missing from these benchmarks? We made it easy to add additional modules to our benchmarking:

1. Add the dependency to ``tox.ini``
1. Add the import statement and the parse statement for the module to ``ISO_8601_MODULES`` in `perform_comparison.py`_

`Submit a pull request`_ and we'll probably add it to our official benchmarks.

.. _`Submit a pull request`: https://github.com/closeio/ciso8601/blob/master/CONTRIBUTING.md
