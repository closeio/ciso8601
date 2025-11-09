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
    |ciso8601                        |69.3 nsec  |60.4 nsec  |64.8 nsec  |59.5 nsec  |N/A                                               |…|89.4 nsec  |85.7 nsec |93.5 nsec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |backports.datetime_fromisoformat|N/A        |N/A        |N/A        |N/A        |0.9x                                              |…|76.4 nsec  |71.6 nsec |79 nsec   |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |datetime (builtin)              |125 nsec   |123 nsec   |136 nsec   |127 nsec   |1.8x                                              |…|N/A        |N/A       |N/A       |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |udatetime                       |543 nsec   |543 nsec   |538 nsec   |520 nsec   |7.8x                                              |…|544 nsec   |544 nsec  |553 nsec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |python-dateutil                 |3.14 usec  |3.41 usec  |4.03 usec  |3.46 usec  |45.3x                                             |…|4.14 usec  |4.16 usec |4.22 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |str2date                        |3.21 usec  |3.28 usec  |3.61 usec  |3.51 usec  |46.3x                                             |…|3.76 usec  |3.71 usec |3.91 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |pendulum                        |4.19 usec  |152 nsec   |126 nsec   |136 nsec   |60.4x                                             |…|148 nsec   |145 nsec  |181 nsec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |iso8601utils                    |N/A        |N/A        |N/A        |N/A        |53.9x                                             |…|N/A        |4.62 usec |5.05 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |iso8601                         |4.97 usec  |5.14 usec  |5.37 usec  |5.33 usec  |71.6x                                             |…|5.21 usec  |5.25 usec |5.7 usec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |isodate                         |5.24 usec  |5.72 usec  |5.9 usec   |5.53 usec  |75.6x                                             |…|5.61 usec  |5.81 usec |6.07 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |PySO8601                        |9.56 usec  |10.2 usec  |9.53 usec  |7.99 usec  |137.9x                                            |…|9.53 usec  |9.98 usec |27.8 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |aniso8601                       |12.2 usec  |12.3 usec  |12.9 usec  |11.7 usec  |175.7x                                            |…|15.5 usec  |16 usec   |15.7 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |zulu                            |12.4 usec  |12.5 usec  |13.8 usec  |13.1 usec  |178.3x                                            |…|14.3 usec  |14.6 usec |14.3 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |arrow                           |42.5 usec  |42.9 usec  |42.4 usec  |42.5 usec  |612.6x                                            |…|49.8 usec  |50.1 usec |49.1 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |maya                            |46.6 usec  |35.4 usec  |42.5 usec  |39.1 usec  |671.5x                                            |…|44.1 usec  |44.8 usec |46.7 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |metomi-isodatetime              |808 usec   |852 usec   |810 usec   |831 usec   |11647.5x                                          |…|1.1 msec   |1.09 msec |1.11 msec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |moment                          |1.22 msec  |1.3 msec   |1.3 msec   |1.38 msec  |17631.5x                                          |…|1.36 msec  |1.4 msec  |1.39 msec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+

ciso8601 takes 69.3 nsec, which is **1.8x faster than datetime (builtin)**, the next fastest Python 3.14 parser in this comparison.

.. </include:benchmark_with_no_time_zone.rst>

Parsing a timestamp with time zone information (e.g., ``2014-01-09T21:48:00-05:30``):

.. <include:benchmark_with_time_zone.rst>

.. table::

    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |             Module             |Python 3.14|Python 3.13|Python 3.12|Python 3.11|Relative slowdown (versus ciso8601, latest Python)|…|Python 3.10|Python 3.9|Python 3.8|
    +================================+===========+===========+===========+===========+==================================================+=+===========+==========+==========+
    |ciso8601                        |71.8 nsec  |70.3 nsec  |75.1 nsec  |67.3 nsec  |N/A                                               |…|98.3 nsec  |92.9 nsec |97.8 nsec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |backports.datetime_fromisoformat|N/A        |N/A        |N/A        |N/A        |1.1x                                              |…|103 nsec   |99.1 nsec |102 nsec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |datetime (builtin)              |197 nsec   |197 nsec   |199 nsec   |179 nsec   |2.7x                                              |…|N/A        |N/A       |N/A       |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |udatetime                       |661 nsec   |638 nsec   |664 nsec   |643 nsec   |9.2x                                              |…|669 nsec   |664 nsec  |669 nsec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |str2date                        |4.04 usec  |3.91 usec  |4.38 usec  |4.49 usec  |56.2x                                             |…|4.66 usec  |4.81 usec |4.9 usec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |python-dateutil                 |4.95 usec  |5.61 usec  |6.33 usec  |5.73 usec  |68.9x                                             |…|6.87 usec  |6.85 usec |7.17 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |pendulum                        |6.53 usec  |202 nsec   |200 nsec   |210 nsec   |91.0x                                             |…|222 nsec   |221 nsec  |262 nsec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |isodate                         |7.5 usec   |7.79 usec  |8.26 usec  |7.74 usec  |104.4x                                            |…|7.76 usec  |7.8 usec  |8.4 usec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |iso8601                         |7.79 usec  |7.71 usec  |8.37 usec  |7.92 usec  |108.4x                                            |…|7.65 usec  |7.69 usec |7.98 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |iso8601utils                    |N/A        |N/A        |N/A        |N/A        |143.3x                                            |…|N/A        |13.3 usec |14.4 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |PySO8601                        |15.8 usec  |16 usec    |16.7 usec  |14.6 usec  |219.7x                                            |…|16.1 usec  |16.2 usec |16.7 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |zulu                            |16.6 usec  |16.2 usec  |17.1 usec  |15.9 usec  |230.9x                                            |…|17.2 usec  |17.2 usec |17.4 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |aniso8601                       |17.6 usec  |17.8 usec  |19 usec    |17.4 usec  |244.8x                                            |…|21.7 usec  |22.8 usec |22.8 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |arrow                           |49 usec    |52.1 usec  |52 usec    |49.7 usec  |682.3x                                            |…|58.8 usec  |58 usec   |58.5 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |maya                            |54.2 usec  |41.4 usec  |44.6 usec  |39.6 usec  |755.5x                                            |…|45.3 usec  |45.7 usec |46.1 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |metomi-isodatetime              |794 usec   |870 usec   |806 usec   |806 usec   |11055.0x                                          |…|1.1 msec   |1.09 msec |1.15 msec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+
    |moment                          |❌         |❌         |❌         |❌         |2163866.8x                                        |…|❌         |❌        |❌        |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+-----------+----------+----------+

ciso8601 takes 71.8 nsec, which is **2.7x faster than datetime (builtin)**, the next fastest Python 3.14 parser in this comparison.

.. </include:benchmark_with_time_zone.rst>

.. <include:benchmark_module_versions.rst>

Tested on Linux 6.17.4-orbstack-00308-g195e9689a04f using the following modules:

.. code:: python

  aniso8601==10.0.1
  arrow==1.4.0
  backports.datetime_fromisoformat==2.0.3
  ciso8601==2.3.3
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
