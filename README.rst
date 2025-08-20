========
ciso8601
========

.. image:: https://img.shields.io/circleci/project/github/closeio/ciso8601.svg
    :target: https://circleci.com/gh/closeio/ciso8601/tree/master

.. image:: https://img.shields.io/pypi/v/ciso8601.svg
    :target: https://pypi.org/project/ciso8601/

.. image:: https://img.shields.io/pypi/pyversions/ciso8601.svg
    :target: https://pypi.org/project/ciso8601/

``ciso8601`` converts `ISO 8601`_ or `RFC 3339`_ date time strings into Python datetime objects.

Since it's written as a C module, it is much faster than other Python libraries.
Tested with cPython 2.7, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14.

.. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601
.. _RFC 3339: https://tools.ietf.org/html/rfc3339

(Interested in working on projects like this? `Close`_ is looking for `great engineers`_ to join our team)

.. _Close: https://close.com
.. _great engineers: https://jobs.close.com


.. contents:: Contents


Quick start
-----------

.. code:: bash

  % pip install ciso8601

.. code:: python

  In [1]: import ciso8601

  In [2]: ciso8601.parse_datetime('2014-12-05T12:30:45.123456-05:30')
  Out[2]: datetime.datetime(2014, 12, 5, 12, 30, 45, 123456, tzinfo=pytz.FixedOffset(330))

  In [3]: ciso8601.parse_datetime('20141205T123045')
  Out[3]: datetime.datetime(2014, 12, 5, 12, 30, 45)

Migration to v2
---------------

Version 2.0.0 of ``ciso8601`` changed the core implementation. This was not entirely backwards compatible, and care should be taken when migrating
See `CHANGELOG`_ for the Migration Guide.

.. _CHANGELOG: https://github.com/closeio/ciso8601/blob/master/CHANGELOG.md

When should I not use ``ciso8601``?
-----------------------------------

``ciso8601`` is not necessarily the best solution for every use case (especially since Python 3.11). See `Should I use ciso8601?`_

.. _`Should I use ciso8601?`: https://github.com/closeio/ciso8601/blob/master/why_ciso8601.md

Error handling
--------------

Starting in v2.0.0, ``ciso8601`` offers strong guarantees when it comes to parsing strings.

``parse_datetime(dt: String): datetime`` is a function that takes a string and either:

* Returns a properly parsed Python datetime, **if and only if** the **entire** string conforms to the supported subset of ISO 8601
* Raises a ``ValueError`` with a description of the reason why the string doesn't conform to the supported subset of ISO 8601

If time zone information is provided, an aware datetime object will be returned. Otherwise, a naive datetime is returned.

Benchmark
---------

Parsing a timestamp with no time zone information (e.g., ``2014-01-09T21:48:00``):

.. <include:benchmark_with_no_time_zone.rst>

.. table::

    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |             Module             |Python 3.14|Python 3.13|Python 3.12|Python 3.11|Relative slowdown (versus ciso8601, latest Python)|…|Python 3.10|Python 3.9|Python 3.8|
    +================================+===========+===========+===========+===========+==================================================+=+===========+==========+==========+
    |ciso8601                        |26.4 nsec  |23.4 nsec  |24.5 nsec  |25.4 nsec  |N/A                                               |…|35.9 nsec  |35.6 nsec |37 nsec   |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |backports.datetime_fromisoformat|N/A        |N/A        |N/A        |N/A        |0.8x                                              |…|30.3 nsec  |30.7 nsec |32 nsec   |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |datetime (builtin)              |51.5 nsec  |48 nsec    |54.8 nsec  |53.9 nsec  |2.0x                                              |…|N/A        |N/A       |N/A       |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |udatetime                       |269 nsec   |277 nsec   |277 nsec   |280 nsec   |10.2x                                             |…|280 nsec   |279 nsec  |280 nsec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |str2date                        |1.4 usec   |1.42 usec  |1.59 usec  |1.59 usec  |52.9x                                             |…|1.62 usec  |1.64 usec |1.76 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |pendulum                        |1.74 usec  |65.2 nsec  |64.8 nsec  |64.7 nsec  |65.8x                                             |…|64.6 nsec  |66.4 nsec |86.4 nsec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |iso8601                         |2.13 usec  |2.2 usec   |2.35 usec  |2.1 usec   |80.6x                                             |…|2.3 usec   |2.31 usec |2.47 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |iso8601utils                    |N/A        |N/A        |N/A        |N/A        |61.5x                                             |…|N/A        |2.19 usec |2.51 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |isodate                         |2.36 usec  |2.52 usec  |2.78 usec  |2.18 usec  |89.3x                                             |…|2.41 usec  |2.4 usec  |2.49 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |PySO8601                        |3.55 usec  |3.79 usec  |3.79 usec  |3.11 usec  |134.6x                                            |…|3.94 usec  |3.64 usec |6.79 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |aniso8601                       |4.32 usec  |4.74 usec  |4.95 usec  |4.37 usec  |163.9x                                            |…|5.53 usec  |5.19 usec |5.72 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |zulu                            |4.71 usec  |4.63 usec  |5.12 usec  |4.54 usec  |178.7x                                            |…|5.17 usec  |4.93 usec |5.17 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |python-dateutil                 |10.3 usec  |11.4 usec  |12.6 usec  |11.9 usec  |390.4x                                            |…|14.9 usec  |15.3 usec |15.8 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |arrow                           |13.3 usec  |13.4 usec  |14.7 usec  |13.5 usec  |503.5x                                            |…|16.7 usec  |16.2 usec |17.4 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |maya                            |13.7 usec  |10.9 usec  |14.7 usec  |12.7 usec  |520.0x                                            |…|15.7 usec  |14.5 usec |16 usec   |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |metomi-isodatetime              |335 usec   |345 usec   |353 usec   |359 usec   |12687.0x                                          |…|480 usec   |468 usec  |508 usec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |moment                          |487 usec   |502 usec   |525 usec   |503 usec   |18471.2x                                          |…|563 usec   |559 usec  |576 usec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+

ciso8601 takes 26.4 nsec, which is **2.0x faster than datetime (builtin)**, the next fastest Python 3.14 parser in this comparison.

.. </include:benchmark_with_no_time_zone.rst>

Parsing a timestamp with time zone information (e.g., ``2014-01-09T21:48:00-05:30``):

.. <include:benchmark_with_time_zone.rst>

.. table::

    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |             Module             |Python 3.14|Python 3.13|Python 3.12|Python 3.11|Relative slowdown (versus ciso8601, latest Python)|…|Python 3.10|Python 3.9|Python 3.8|
    +================================+===========+===========+===========+===========+==================================================+=+===========+==========+==========+
    |ciso8601                        |30.7 nsec  |27.8 nsec  |27.9 nsec  |29.3 nsec  |N/A                                               |…|39 nsec    |39.4 nsec |40.2 nsec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |backports.datetime_fromisoformat|N/A        |N/A        |N/A        |N/A        |1.2x                                              |…|46.6 nsec  |48.4 nsec |49.1 nsec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |datetime (builtin)              |81.6 nsec  |72.7 nsec  |77.8 nsec  |68.8 nsec  |2.7x                                              |…|N/A        |N/A       |N/A       |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |udatetime                       |344 nsec   |321 nsec   |334 nsec   |332 nsec   |11.2x                                             |…|331 nsec   |332 nsec  |336 nsec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |str2date                        |1.67 usec  |1.73 usec  |1.94 usec  |1.77 usec  |54.2x                                             |…|1.96 usec  |1.94 usec |2.08 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |pendulum                        |2.48 usec  |104 nsec   |104 nsec   |104 nsec   |80.7x                                             |…|106 nsec   |105 nsec  |130 nsec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |iso8601                         |3.04 usec  |3.24 usec  |3.42 usec  |3.06 usec  |98.7x                                             |…|3.17 usec  |3.18 usec |3.52 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |isodate                         |3.14 usec  |3.16 usec  |3.39 usec  |2.88 usec  |102.3x                                            |…|3.1 usec   |3.12 usec |3.26 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |iso8601utils                    |N/A        |N/A        |N/A        |N/A        |126.4x                                            |…|N/A        |4.98 usec |5.3 usec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |PySO8601                        |5.11 usec  |5.23 usec  |5.67 usec  |4.75 usec  |166.3x                                            |…|5.31 usec  |5.23 usec |5.72 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |zulu                            |5.47 usec  |5.66 usec  |6.08 usec  |5.26 usec  |177.9x                                            |…|5.85 usec  |5.83 usec |5.96 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |aniso8601                       |5.96 usec  |6.42 usec  |7.19 usec  |6.18 usec  |194.0x                                            |…|7.56 usec  |7.26 usec |7.91 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |python-dateutil                 |13.2 usec  |14.6 usec  |15.6 usec  |15.9 usec  |428.8x                                            |…|19.7 usec  |20 usec   |20.6 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |arrow                           |15.6 usec  |16.3 usec  |19.5 usec  |16.1 usec  |507.7x                                            |…|20 usec    |19.3 usec |19.9 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |maya                            |15.8 usec  |12 usec    |14.4 usec  |12.4 usec  |512.7x                                            |…|15 usec    |14.7 usec |15.1 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |metomi-isodatetime              |329 usec   |346 usec   |342 usec   |335 usec   |10692.8x                                          |…|475 usec   |482 usec  |487 usec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |moment                          |❌         |❌         |❌         |❌         |2112732.4x                                        |…|❌         |❌        |❌        |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+

ciso8601 takes 30.7 nsec, which is **2.7x faster than datetime (builtin)**, the next fastest Python 3.14 parser in this comparison.

.. </include:benchmark_with_time_zone.rst>

.. <include:benchmark_module_versions.rst>

Tested on Linux 6.14.10-orbstack-00291-g1b252bd3edea using the following modules:

.. code:: python

  aniso8601==10.0.1
  arrow==1.3.0
  backports.datetime_fromisoformat==2.0.3
  ciso8601==2.3.2
  iso8601==2.1.0
  iso8601utils==0.1.2
  isodate==0.7.2
  maya==0.6.1
  metomi-isodatetime==1!3.1.0
  moment==0.12.1
  pendulum==3.1.0 (on Python 3.9, 3.10, 3.11, 3.12, 3.13, 3.14), pendulum==3.0.0 (on Python 3.8)
  PySO8601==0.2.0
  python-dateutil==2.9.0.post0
  str2date==0.905
  udatetime==0.0.17
  zulu==2.0.1

.. </include:benchmark_module_versions.rst>

For full benchmarking details (or to run the benchmark yourself), see `benchmarking/README.rst`_

.. _`benchmarking/README.rst`: https://github.com/closeio/ciso8601/blob/master/benchmarking/README.rst

Supported subset of ISO 8601
----------------------------

.. |datetime.fromisoformat| replace:: ``datetime.fromisoformat``
.. _datetime.fromisoformat: https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat

``ciso8601`` only supports a subset of ISO 8601, but supports a superset of what is supported by Python itself (|datetime.fromisoformat|_), and supports the entirety of the `RFC 3339`_ specification.

Date formats
^^^^^^^^^^^^

The following date formats are supported:

.. table::
   :widths: auto

   ============================= ============== ==================
   Format                        Example        Supported
   ============================= ============== ==================
   ``YYYY-MM-DD`` (extended)     ``2018-04-29`` ✅
   ``YYYY-MM`` (extended)        ``2018-04``    ✅
   ``YYYYMMDD`` (basic)          ``20180429``   ✅
   ``YYYY-Www-D`` (week date)    ``2009-W01-1`` ✅
   ``YYYY-Www`` (week date)      ``2009-W01``   ✅
   ``YYYYWwwD`` (week date)      ``2009W011``   ✅
   ``YYYYWww`` (week date)       ``2009W01``    ✅
   ``YYYY-DDD`` (ordinal date)   ``1981-095``   ✅
   ``YYYYDDD`` (ordinal date)    ``1981095``    ✅
   ============================= ============== ==================

Uncommon ISO 8601 date formats are not supported:

.. table::
   :widths: auto

   ============================= ============== ==================
   Format                        Example        Supported
   ============================= ============== ==================
   ``--MM-DD`` (omitted year)    ``--04-29``    ❌
   ``--MMDD`` (omitted year)     ``--0429``     ❌
   ``±YYYYY-MM`` (>4 digit year) ``+10000-04``  ❌
   ``+YYYY-MM`` (leading +)      ``+2018-04``   ❌
   ``-YYYY-MM`` (negative -)     ``-2018-04``   ❌
   ============================= ============== ==================

Time formats
^^^^^^^^^^^^

Times are optional and are separated from the date by the letter ``T``.

Consistent with `RFC 3339`__, ``ciso8601`` also allows either a space character, or a lower-case ``t``, to be used instead of a ``T``.

__ https://stackoverflow.com/questions/522251/whats-the-difference-between-iso-8601-and-rfc-3339-date-formats

The following time formats are supported:

.. table::
   :widths: auto

   =================================== =================== ==============
   Format                              Example             Supported
   =================================== =================== ==============
   ``hh``                              ``11``              ✅
   ``hhmm``                            ``1130``            ✅
   ``hh:mm``                           ``11:30``           ✅
   ``hhmmss``                          ``113059``          ✅
   ``hh:mm:ss``                        ``11:30:59``        ✅
   ``hhmmss.ssssss``                   ``113059.123456``   ✅
   ``hh:mm:ss.ssssss``                 ``11:30:59.123456`` ✅
   ``hhmmss,ssssss``                   ``113059,123456``   ✅
   ``hh:mm:ss,ssssss``                 ``11:30:59,123456`` ✅
   Midnight (special case)             ``24:00:00``        ✅
   ``hh.hhh`` (fractional hours)       ``11.5``            ❌
   ``hh:mm.mmm`` (fractional minutes)  ``11:30.5``         ❌
   =================================== =================== ==============

**Note:** Python datetime objects only have microsecond precision (6 digits). Any additional precision will be truncated.

Time zone information
^^^^^^^^^^^^^^^^^^^^^

Time zone information may be provided in one of the following formats:

.. table::
   :widths: auto

   ========== ========== ===========
   Format     Example    Supported
   ========== ========== ===========
   ``Z``      ``Z``      ✅
   ``z``      ``z``      ✅
   ``±hh``    ``+11``    ✅
   ``±hhmm``  ``+1130``  ✅
   ``±hh:mm`` ``+11:30`` ✅
   ========== ========== ===========

While the ISO 8601 specification allows the use of MINUS SIGN (U+2212) in the time zone separator, ``ciso8601`` only supports the use of the HYPHEN-MINUS (U+002D) character.

Consistent with `RFC 3339`_, ``ciso8601`` also allows a lower-case ``z`` to be used instead of a ``Z``.

Strict RFC 3339 parsing
-----------------------

``ciso8601`` parses ISO 8601 datetimes, which can be thought of as a superset of `RFC 3339`_ (`roughly`_). In cases where you might want strict RFC 3339 parsing, ``ciso8601`` offers a ``parse_rfc3339`` method, which behaves in a similar manner to ``parse_datetime``:

.. _roughly: https://stackoverflow.com/questions/522251/whats-the-difference-between-iso-8601-and-rfc-3339-date-formats

``parse_rfc3339(dt: String): datetime`` is a function that takes a string and either:

* Returns a properly parsed Python datetime, **if and only if** the **entire** string conforms to RFC 3339.
* Raises a ``ValueError`` with a description of the reason why the string doesn't conform to RFC 3339.

Ignoring time zone information while parsing
--------------------------------------------

It takes more time to parse timestamps with time zone information, especially if they're not in UTC. However, there are times when you don't care about time zone information, and wish to produce naive datetimes instead.
For example, if you are certain that your program will only parse timestamps from a single time zone, you might want to strip the time zone information and only output naive datetimes.

In these limited cases, there is a second function provided.
``parse_datetime_as_naive`` will ignore any time zone information it finds and, as a result, is faster for timestamps containing time zone information.

.. code:: python

  In [1]: import ciso8601

  In [2]: ciso8601.parse_datetime_as_naive('2014-12-05T12:30:45.123456-05:30')
  Out[2]: datetime.datetime(2014, 12, 5, 12, 30, 45, 123456)

NOTE: ``parse_datetime_as_naive`` is only useful in the case where your timestamps have time zone information, but you want to ignore it. This is somewhat unusual.
If your timestamps don't have time zone information (i.e. are naive), simply use ``parse_datetime``. It is just as fast.
