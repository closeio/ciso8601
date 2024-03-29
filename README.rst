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
Tested with cPython 2.7, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12.

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

    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |             Module             |Python 3.12|Python 3.11|Python 3.10|Python 3.9|Relative slowdown (versus ciso8601, latest Python)|…|Python 3.8|Python 3.7|          Python 2.7           |
    +================================+===========+===========+===========+==========+==================================================+=+==========+==========+===============================+
    |ciso8601                        |98 nsec    |90 nsec    |122 nsec   |122 nsec  |N/A                                               |…|118 nsec  |124 nsec  |134 nsec                       |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |backports.datetime_fromisoformat|N/A        |N/A        |112 nsec   |108 nsec  |0.9x                                              |…|106 nsec  |118 nsec  |N/A                            |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |datetime (builtin)              |129 nsec   |132 nsec   |N/A        |N/A       |1.3x                                              |…|N/A       |N/A       |N/A                            |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |pendulum                        |N/A        |180 nsec   |187 nsec   |186 nsec  |2.0x                                              |…|196 nsec  |200 nsec  |8.52 usec                      |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |udatetime                       |695 nsec   |662 nsec   |674 nsec   |692 nsec  |7.1x                                              |…|724 nsec  |713 nsec  |586 nsec                       |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |str2date                        |6.86 usec  |5.78 usec  |6.59 usec  |6.4 usec  |70.0x                                             |…|6.66 usec |6.96 usec |❌                             |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |iso8601utils                    |N/A        |N/A        |N/A        |8.59 usec |70.5x                                             |…|8.6 usec  |9.59 usec |11.2 usec                      |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |iso8601                         |10 usec    |8.24 usec  |8.96 usec  |9.21 usec |102.2x                                            |…|9.14 usec |9.63 usec |25.7 usec                      |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |isodate                         |11.1 usec  |8.76 usec  |10.2 usec  |9.76 usec |113.6x                                            |…|9.92 usec |11 usec   |44.1 usec                      |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |PySO8601                        |17.2 usec  |13.6 usec  |16 usec    |15.8 usec |175.3x                                            |…|16.1 usec |17.1 usec |17.7 usec                      |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |aniso8601                       |22.2 usec  |17.8 usec  |23.2 usec  |23.1 usec |227.0x                                            |…|24.3 usec |27.2 usec |30.7 usec                      |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |zulu                            |23.3 usec  |19 usec    |22 usec    |21.3 usec |237.9x                                            |…|21.6 usec |22.7 usec |N/A                            |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |maya                            |N/A        |36.1 usec  |42.5 usec  |42.7 usec |401.6x                                            |…|41.3 usec |44.2 usec |N/A                            |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |python-dateutil                 |57.6 usec  |51.4 usec  |63.3 usec  |62.6 usec |587.7x                                            |…|63.7 usec |67.3 usec |119 usec                       |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |arrow                           |62 usec    |54 usec    |65.5 usec  |65.7 usec |633.0x                                            |…|66.6 usec |70.2 usec |78.8 usec                      |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |metomi-isodatetime              |1.29 msec  |1.33 msec  |1.76 msec  |1.77 msec |13201.1x                                          |…|1.79 msec |1.91 msec |N/A                            |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |moment                          |1.81 msec  |1.65 msec  |1.75 msec  |1.79 msec |18474.8x                                          |…|1.78 msec |1.84 msec |N/A                            |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+

ciso8601 takes 98 nsec, which is **1.3x faster than datetime (builtin)**, the next fastest Python 3.12 parser in this comparison.

.. </include:benchmark_with_no_time_zone.rst>

Parsing a timestamp with time zone information (e.g., ``2014-01-09T21:48:00-05:30``):

.. <include:benchmark_with_time_zone.rst>

.. table::

    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |             Module             |Python 3.12|Python 3.11|Python 3.10|Python 3.9|Relative slowdown (versus ciso8601, latest Python)|…|Python 3.8|Python 3.7|          Python 2.7           |
    +================================+===========+===========+===========+==========+==================================================+=+==========+==========+===============================+
    |ciso8601                        |95 nsec    |96.8 nsec  |128 nsec   |123 nsec  |N/A                                               |…|125 nsec  |125 nsec  |140 nsec                       |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |backports.datetime_fromisoformat|N/A        |N/A        |147 nsec   |149 nsec  |1.1x                                              |…|138 nsec  |149 nsec  |N/A                            |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |datetime (builtin)              |198 nsec   |207 nsec   |N/A        |N/A       |2.1x                                              |…|N/A       |N/A       |N/A                            |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |pendulum                        |N/A        |225 nsec   |214 nsec   |211 nsec  |2.3x                                              |…|219 nsec  |224 nsec  |13.5 usec                      |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |udatetime                       |799 nsec   |803 nsec   |805 nsec   |830 nsec  |8.4x                                              |…|827 nsec  |805 nsec  |768 nsec                       |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |str2date                        |7.73 usec  |6.75 usec  |7.78 usec  |7.8 usec  |81.4x                                             |…|7.74 usec |8.13 usec |❌                             |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |iso8601                         |13.7 usec  |11.3 usec  |12.7 usec  |12.5 usec |143.8x                                            |…|12.4 usec |12.6 usec |31.1 usec                      |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |isodate                         |13.7 usec  |11.3 usec  |12.9 usec  |12.7 usec |144.0x                                            |…|12.7 usec |13.9 usec |46.7 usec                      |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |iso8601utils                    |N/A        |N/A        |N/A        |21.4 usec |174.9x                                            |…|22.1 usec |23.4 usec |28.3 usec                      |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |PySO8601                        |25.1 usec  |20.4 usec  |23.2 usec  |23.8 usec |263.8x                                            |…|23.5 usec |24.8 usec |25.3 usec                      |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |zulu                            |26.3 usec  |21.4 usec  |25.7 usec  |24 usec   |277.2x                                            |…|24.5 usec |25.3 usec |N/A                            |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |aniso8601                       |27.7 usec  |23.7 usec  |30.3 usec  |30 usec   |291.3x                                            |…|31.6 usec |33.8 usec |39.2 usec                      |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |maya                            |N/A        |36 usec    |41.3 usec  |41.8 usec |372.0x                                            |…|42.4 usec |42.7 usec |N/A                            |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |python-dateutil                 |70.7 usec  |65.1 usec  |77.9 usec  |80.2 usec |744.0x                                            |…|79.4 usec |83.6 usec |100 usec                       |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |arrow                           |73 usec    |62.8 usec  |74.5 usec  |73.9 usec |768.6x                                            |…|75.1 usec |80 usec   |148 usec                       |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |metomi-isodatetime              |1.22 msec  |1.25 msec  |1.72 msec  |1.72 msec |12876.3x                                          |…|1.76 msec |1.83 msec |N/A                            |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+
    |moment                          |❌         |❌         |❌         |❌        |2305822.8x                                        |…|❌        |❌        |N/A                            |
    +--------------------------------+-----------+-----------+-----------+----------+--------------------------------------------------+-+----------+----------+-------------------------------+

ciso8601 takes 95 nsec, which is **2.1x faster than datetime (builtin)**, the next fastest Python 3.12 parser in this comparison.

.. </include:benchmark_with_time_zone.rst>

.. <include:benchmark_module_versions.rst>

Tested on Linux 5.15.49-linuxkit using the following modules:

.. code:: python

  aniso8601==9.0.1
  arrow==1.3.0 (on Python 3.8, 3.9, 3.10, 3.11, 3.12), arrow==1.2.3 (on Python 3.7), arrow==0.17.0 (on Python 2.7)
  backports.datetime_fromisoformat==2.0.1
  ciso8601==2.3.0
  iso8601==2.1.0 (on Python 3.8, 3.9, 3.10, 3.11, 3.12), iso8601==0.1.16 (on Python 2.7)
  iso8601utils==0.1.2
  isodate==0.6.1
  maya==0.6.1
  metomi-isodatetime==1!3.1.0
  moment==0.12.1
  pendulum==2.1.2
  PySO8601==0.2.0
  python-dateutil==2.8.2
  str2date==0.905
  udatetime==0.0.17
  zulu==2.0.0

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
