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

    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |             Module             |Python 3.12|Python 3.11|Python 3.10|Python 3.9|Python 3.8|Python 3.7|          Python 2.7           |Relative slowdown (versus ciso8601, latest Python)|
    +================================+===========+===========+===========+==========+==========+==========+===============================+==================================================+
    |ciso8601                        |94.4 nsec  |89.2 nsec  |125 nsec   |117 nsec  |129 nsec  |122 nsec  |134 nsec                       |N/A                                               |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |backports.datetime_fromisoformat|N/A        |N/A        |112 nsec   |105 nsec  |106 nsec  |112 nsec  |N/A                            |0.9x                                              |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |datetime (builtin)              |129 nsec   |136 nsec   |N/A        |N/A       |N/A       |N/A       |N/A                            |1.4x                                              |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |pendulum                        |N/A        |184 nsec   |191 nsec   |191 nsec  |192 nsec  |204 nsec  |8.52 usec                      |2.1x                                              |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |udatetime                       |709 nsec   |677 nsec   |692 nsec   |715 nsec  |705 nsec  |700 nsec  |586 nsec                       |7.5x                                              |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |str2date                        |6.84 usec  |5.8 usec   |6.86 usec  |6.6 usec  |6.47 usec |6.89 usec |**Incorrect Result** (``None``)|72.5x                                             |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |iso8601utils                    |N/A        |N/A        |N/A        |8.64 usec |8.69 usec |9.2 usec  |11.2 usec                      |74.0x                                             |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |iso8601                         |9.41 usec  |8.06 usec  |9.2 usec   |9.05 usec |9.35 usec |9.38 usec |25.7 usec                      |99.6x                                             |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |isodate                         |10.5 usec  |8.68 usec  |10.2 usec  |9.68 usec |10.1 usec |10.9 usec |44.1 usec                      |111.4x                                            |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |PySO8601                        |17.1 usec  |13.4 usec  |16.4 usec  |16.1 usec |16.6 usec |17.1 usec |17.7 usec                      |181.2x                                            |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |aniso8601                       |21.7 usec  |18.1 usec  |24 usec    |23.3 usec |23.7 usec |27.6 usec |30.7 usec                      |229.6x                                            |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |zulu                            |23.5 usec  |20.1 usec  |22.4 usec  |21.3 usec |21.8 usec |22.2 usec |N/A                            |248.7x                                            |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |maya                            |N/A        |37.4 usec  |42.4 usec  |42.1 usec |42.2 usec |43 usec   |N/A                            |419.4x                                            |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |python-dateutil                 |55.5 usec  |51.6 usec  |63 usec    |62.9 usec |65.4 usec |67.8 usec |119 usec                       |588.0x                                            |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |arrow                           |62.7 usec  |54.4 usec  |65.5 usec  |64.6 usec |65 usec   |71.2 usec |78.8 usec                      |664.2x                                            |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |metomi-isodatetime              |1.31 msec  |1.3 msec   |1.76 msec  |1.78 msec |1.78 msec |1.91 msec |N/A                            |13823.8x                                          |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |moment                          |1.79 msec  |1.73 msec  |1.77 msec  |1.75 msec |1.79 msec |1.95 msec |N/A                            |18962.8x                                          |
    +--------------------------------+-----------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+

ciso8601 takes 94.4 nsec, which is **1.4x faster than datetime (builtin)**, the next fastest Python 3.12 parser in this comparison.

.. </include:benchmark_with_no_time_zone.rst>

Parsing a timestamp with time zone information (e.g., ``2014-01-09T21:48:00-05:30``):

.. <include:benchmark_with_time_zone.rst>

.. table::

    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |             Module             |          Python 3.12          |          Python 3.11          |          Python 3.10          |          Python 3.9           |          Python 3.8           |          Python 3.7           |          Python 2.7           |Relative slowdown (versus ciso8601, latest Python)|
    +================================+===============================+===============================+===============================+===============================+===============================+===============================+===============================+==================================================+
    |ciso8601                        |106 nsec                       |97 nsec                        |129 nsec                       |125 nsec                       |118 nsec                       |132 nsec                       |140 nsec                       |N/A                                               |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |backports.datetime_fromisoformat|N/A                            |N/A                            |148 nsec                       |142 nsec                       |139 nsec                       |148 nsec                       |N/A                            |1.1x                                              |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |datetime (builtin)              |197 nsec                       |203 nsec                       |N/A                            |N/A                            |N/A                            |N/A                            |N/A                            |1.9x                                              |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |pendulum                        |N/A                            |210 nsec                       |214 nsec                       |209 nsec                       |216 nsec                       |225 nsec                       |13.5 usec                      |2.2x                                              |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |udatetime                       |828 nsec                       |785 nsec                       |805 nsec                       |811 nsec                       |798 nsec                       |816 nsec                       |768 nsec                       |7.8x                                              |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |str2date                        |7.79 usec                      |6.86 usec                      |7.71 usec                      |7.77 usec                      |7.62 usec                      |8 usec                         |**Incorrect Result** (``None``)|73.6x                                             |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |iso8601                         |12.9 usec                      |11.6 usec                      |13.1 usec                      |12.4 usec                      |12.9 usec                      |12.6 usec                      |31.1 usec                      |121.7x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |isodate                         |13.6 usec                      |11.6 usec                      |13 usec                        |12.5 usec                      |12.9 usec                      |13.7 usec                      |46.7 usec                      |128.5x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |iso8601utils                    |N/A                            |N/A                            |N/A                            |20.8 usec                      |22.5 usec                      |23.5 usec                      |28.3 usec                      |166.8x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |PySO8601                        |25.9 usec                      |20.5 usec                      |22.8 usec                      |24 usec                        |23.7 usec                      |24.3 usec                      |25.3 usec                      |244.4x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |zulu                            |26.3 usec                      |21.9 usec                      |25 usec                        |24.2 usec                      |24.9 usec                      |25.1 usec                      |N/A                            |248.8x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |aniso8601                       |28 usec                        |25.4 usec                      |30.2 usec                      |29.7 usec                      |31.4 usec                      |33.8 usec                      |39.2 usec                      |264.4x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |maya                            |N/A                            |36.5 usec                      |41.3 usec                      |41.3 usec                      |40.7 usec                      |42.3 usec                      |N/A                            |376.1x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |python-dateutil                 |70.4 usec                      |64.4 usec                      |78.1 usec                      |78 usec                        |79.3 usec                      |83.3 usec                      |100 usec                       |664.3x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |arrow                           |74.1 usec                      |63.5 usec                      |75 usec                        |74 usec                        |74.7 usec                      |80.9 usec                      |148 usec                       |699.8x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |metomi-isodatetime              |1.24 msec                      |1.33 msec                      |1.73 msec                      |1.73 msec                      |1.73 msec                      |1.86 msec                      |N/A                            |11719.3x                                          |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |moment                          |**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|N/A                            |2116377.5x                                        |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+

ciso8601 takes 106 nsec, which is **1.9x faster than datetime (builtin)**, the next fastest Python 3.12 parser in this comparison.

.. </include:benchmark_with_time_zone.rst>

.. <include:benchmark_module_versions.rst>

Tested on Darwin 22.5.0 using the following modules:

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
