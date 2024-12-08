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
Tested with cPython 2.7, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13.

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

    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |             Module             |Python 3.13|Python 3.12|Python 3.11|Python 3.10|Relative slowdown (versus ciso8601, latest Python)|…|Python 3.9|Python 3.8|
    +================================+===========+===========+===========+===========+==================================================+=+==========+==========+
    |ciso8601                        |64.8 nsec  |62.8 nsec  |60.1 nsec  |91.7 nsec  |N/A                                               |…|86 nsec   |92.9 nsec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |backports.datetime_fromisoformat|N/A        |N/A        |N/A        |73.6 nsec  |0.8x                                              |…|70 nsec   |75.9 nsec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |datetime (builtin)              |147 nsec   |138 nsec   |123 nsec   |N/A        |2.3x                                              |…|N/A       |N/A       |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |pendulum                        |171 nsec   |181 nsec   |175 nsec   |214 nsec   |2.6x                                              |…|179 nsec  |180 nsec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |udatetime                       |542 nsec   |563 nsec   |525 nsec   |555 nsec   |8.4x                                              |…|551 nsec  |553 nsec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |str2date                        |3.29 usec  |3.53 usec  |3.52 usec  |3.85 usec  |50.8x                                             |…|3.72 usec |3.9 usec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |iso8601utils                    |N/A        |N/A        |N/A        |N/A        |56.9x                                             |…|4.89 usec |4.89 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |iso8601                         |5.1 usec   |5.4 usec   |5.18 usec  |5.38 usec  |78.8x                                             |…|5.36 usec |5.55 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |isodate                         |5.76 usec  |5.85 usec  |5.21 usec  |5.91 usec  |89.0x                                             |…|5.97 usec |6.07 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |PySO8601                        |10 usec    |11.5 usec  |7.99 usec  |10.9 usec  |155.0x                                            |…|9.83 usec |9.81 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |aniso8601                       |12.1 usec  |12.5 usec  |11.1 usec  |15.1 usec  |186.9x                                            |…|15.4 usec |15.6 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |zulu                            |12.3 usec  |13.6 usec  |12.6 usec  |14.2 usec  |189.4x                                            |…|14.5 usec |14.2 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |maya                            |35.9 usec  |N/A        |40.6 usec  |46.7 usec  |554.3x                                            |…|45.4 usec |46.3 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |python-dateutil                 |36.2 usec  |36.9 usec  |36.1 usec  |44 usec    |558.5x                                            |…|46.4 usec |45.2 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |arrow                           |42.9 usec  |43.8 usec  |41.2 usec  |48.8 usec  |662.7x                                            |…|50.7 usec |50.1 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |metomi-isodatetime              |828 usec   |822 usec   |791 usec   |1.09 msec  |12781.0x                                          |…|1.1 msec  |1.11 msec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |moment                          |1.28 msec  |1.32 msec  |1.29 msec  |1.36 msec  |19696.9x                                          |…|1.37 msec |1.34 msec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+

ciso8601 takes 64.8 nsec, which is **2.3x faster than datetime (builtin)**, the next fastest Python 3.13 parser in this comparison.

.. </include:benchmark_with_no_time_zone.rst>

Parsing a timestamp with time zone information (e.g., ``2014-01-09T21:48:00-05:30``):

.. <include:benchmark_with_time_zone.rst>

.. table::

    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |             Module             |Python 3.13|Python 3.12|Python 3.11|Python 3.10|Relative slowdown (versus ciso8601, latest Python)|…|Python 3.9|Python 3.8|
    +================================+===========+===========+===========+===========+==================================================+=+==========+==========+
    |ciso8601                        |73.9 nsec  |71 nsec    |65.6 nsec  |97.5 nsec  |N/A                                               |…|92.9 nsec |96.6 nsec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |backports.datetime_fromisoformat|N/A        |N/A        |N/A        |99.2 nsec  |1.0x                                              |…|93 nsec   |99.4 nsec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |datetime (builtin)              |205 nsec   |198 nsec   |178 nsec   |N/A        |2.8x                                              |…|N/A       |N/A       |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |pendulum                        |251 nsec   |259 nsec   |251 nsec   |262 nsec   |3.4x                                              |…|264 nsec  |264 nsec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |udatetime                       |684 nsec   |700 nsec   |646 nsec   |684 nsec   |9.3x                                              |…|688 nsec  |676 nsec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |str2date                        |5.95 usec  |4.34 usec  |4.11 usec  |4.58 usec  |80.5x                                             |…|4.6 usec  |4.82 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |iso8601                         |7.68 usec  |8.56 usec  |7.62 usec  |7.99 usec  |103.9x                                            |…|7.83 usec |8.16 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |isodate                         |7.77 usec  |8.53 usec  |7.54 usec  |7.88 usec  |105.0x                                            |…|8.12 usec |8.4 usec  |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |iso8601utils                    |N/A        |N/A        |N/A        |N/A        |152.2x                                            |…|14.1 usec |14.6 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |zulu                            |17.8 usec  |16.9 usec  |15.7 usec  |17.3 usec  |241.3x                                            |…|17.3 usec |17.6 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |aniso8601                       |18 usec    |18.7 usec  |16.4 usec  |21.5 usec  |243.1x                                            |…|22.5 usec |22.8 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |PySO8601                        |18.3 usec  |16.6 usec  |14.3 usec  |15.8 usec  |247.5x                                            |…|16.2 usec |16.4 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |maya                            |46.2 usec  |N/A        |41 usec    |47.5 usec  |625.0x                                            |…|45.2 usec |47 usec   |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |python-dateutil                 |47.1 usec  |48.2 usec  |47.1 usec  |57.3 usec  |636.5x                                            |…|60.4 usec |58.9 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |arrow                           |57.7 usec  |53.8 usec  |50.8 usec  |60.2 usec  |780.2x                                            |…|59.4 usec |60.1 usec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |metomi-isodatetime              |876 usec   |823 usec   |795 usec   |1.09 msec  |11846.4x                                          |…|1.09 msec |1.13 msec |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+
    |moment                          |❌         |❌         |❌         |❌         |2070678.8x                                        |…|❌        |❌        |
    +--------------------------------+-----------+-----------+-----------+-----------+--------------------------------------------------+-+----------+----------+

ciso8601 takes 73.9 nsec, which is **2.8x faster than datetime (builtin)**, the next fastest Python 3.13 parser in this comparison.

.. </include:benchmark_with_time_zone.rst>

.. <include:benchmark_module_versions.rst>

Tested on Linux 6.11.5-orbstack-00280-g96d99c92a42b using the following modules:

.. code:: python

  aniso8601==9.0.1
  arrow==1.3.0
  backports.datetime_fromisoformat==2.0.2
  ciso8601==2.3.1
  iso8601==2.1.0
  iso8601utils==0.1.2
  isodate==0.7.2
  maya==0.6.1
  metomi-isodatetime==1!3.1.0
  moment==0.12.1
  pendulum==3.0.0
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
