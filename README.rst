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
Tested with cPython 2.7, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11.

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

    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |             Module             |Python 3.11|Python 3.10|Python 3.9|Python 3.8|Python 3.7|          Python 2.7           |Relative slowdown (versus ciso8601, latest Python)|
    +================================+===========+===========+==========+==========+==========+===============================+==================================================+
    |ciso8601                        |84.5 nsec  |111 nsec   |102 nsec  |111 nsec  |112 nsec  |134 nsec                       |N/A                                               |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |backports.datetime_fromisoformat|N/A        |107 nsec   |105 nsec  |117 nsec  |112 nsec  |N/A                            |1.0x                                              |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |datetime (builtin)              |114 nsec   |N/A        |N/A       |N/A       |N/A       |N/A                            |1.4x                                              |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |pendulum                        |174 nsec   |177 nsec   |164 nsec  |201 nsec  |202 nsec  |8.52 usec                      |2.1x                                              |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |udatetime                       |593 nsec   |627 nsec   |640 nsec  |713 nsec  |660 nsec  |586 nsec                       |7.0x                                              |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |str2date                        |5.32 usec  |6.14 usec  |5.88 usec |6.68 usec |6.53 usec |**Incorrect Result** (``None``)|62.9x                                             |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |iso8601                         |7.28 usec  |8.32 usec  |8.12 usec |9.59 usec |8.78 usec |25.7 usec                      |86.1x                                             |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |iso8601utils                    |N/A        |N/A        |7.91 usec |9.28 usec |8.81 usec |11.2 usec                      |77.5x                                             |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |isodate                         |8.21 usec  |9.5 usec   |9.05 usec |10.8 usec |10.5 usec |44.1 usec                      |97.1x                                             |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |PySO8601                        |12.9 usec  |14.8 usec  |15 usec   |17.2 usec |16.3 usec |17.7 usec                      |152.9x                                            |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |aniso8601                       |16.8 usec  |22.1 usec  |21 usec   |23.5 usec |24.7 usec |30.7 usec                      |198.3x                                            |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |zulu                            |18 usec    |21.1 usec  |20.4 usec |22.1 usec |21.2 usec |N/A                            |212.5x                                            |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |maya                            |35.1 usec  |40.7 usec  |40.2 usec |40.1 usec |41.8 usec |N/A                            |415.4x                                            |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |python-dateutil                 |49 usec    |59 usec    |57.4 usec |63 usec   |64.3 usec |119 usec                       |579.6x                                            |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |arrow                           |51.5 usec  |61.6 usec  |60.3 usec |62.8 usec |65.8 usec |78.8 usec                      |609.7x                                            |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |metomi-isodatetime              |1.18 msec  |1.67 msec  |1.64 msec |1.73 msec |1.81 msec |N/A                            |13981.2x                                          |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |moment                          |1.57 msec  |1.62 msec  |1.65 msec |1.7 msec  |1.74 msec |N/A                            |18540.2x                                          |
    +--------------------------------+-----------+-----------+----------+----------+----------+-------------------------------+--------------------------------------------------+

ciso8601 takes 84.5 nsec, which is **1.4x faster than datetime (builtin)**, the next fastest Python 3.11 parser in this comparison.

.. </include:benchmark_with_no_time_zone.rst>

Parsing a timestamp with time zone information (e.g., ``2014-01-09T21:48:00-05:30``):

.. <include:benchmark_with_time_zone.rst>

.. table::

    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |             Module             |          Python 3.11          |          Python 3.10          |          Python 3.9           |          Python 3.8           |          Python 3.7           |          Python 2.7           |Relative slowdown (versus ciso8601, latest Python)|
    +================================+===============================+===============================+===============================+===============================+===============================+===============================+==================================================+
    |ciso8601                        |115 nsec                       |116 nsec                       |109 nsec                       |111 nsec                       |115 nsec                       |140 nsec                       |N/A                                               |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |backports.datetime_fromisoformat|N/A                            |163 nsec                       |146 nsec                       |139 nsec                       |148 nsec                       |N/A                            |1.4x                                              |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |datetime (builtin)              |199 nsec                       |N/A                            |N/A                            |N/A                            |N/A                            |N/A                            |1.7x                                              |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |pendulum                        |205 nsec                       |210 nsec                       |189 nsec                       |209 nsec                       |204 nsec                       |13.5 usec                      |1.8x                                              |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |udatetime                       |745 nsec                       |719 nsec                       |731 nsec                       |726 nsec                       |734 nsec                       |768 nsec                       |6.5x                                              |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |str2date                        |6.78 usec                      |7.55 usec                      |7.67 usec                      |7.69 usec                      |7.47 usec                      |**Incorrect Result** (``None``)|58.8x                                             |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |iso8601                         |11.1 usec                      |12.1 usec                      |12 usec                        |12.3 usec                      |12.2 usec                      |31.1 usec                      |96.1x                                             |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |isodate                         |11.4 usec                      |12.4 usec                      |12.4 usec                      |13 usec                        |13.1 usec                      |46.7 usec                      |98.8x                                             |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |iso8601utils                    |N/A                            |N/A                            |20.3 usec                      |37.8 usec                      |22.7 usec                      |28.3 usec                      |185.5x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |PySO8601                        |20.5 usec                      |22.9 usec                      |23.2 usec                      |23.5 usec                      |24.8 usec                      |25.3 usec                      |178.0x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |zulu                            |25.5 usec                      |24.2 usec                      |23.4 usec                      |23.3 usec                      |24.3 usec                      |N/A                            |221.7x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |aniso8601                       |29.5 usec                      |28.5 usec                      |27.6 usec                      |30.1 usec                      |32.1 usec                      |39.2 usec                      |256.2x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |maya                            |37.1 usec                      |40.4 usec                      |38.9 usec                      |40.3 usec                      |40.9 usec                      |N/A                            |322.0x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |arrow                           |62.7 usec                      |73 usec                        |69.9 usec                      |71.7 usec                      |75.5 usec                      |100 usec                       |544.4x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |python-dateutil                 |64.8 usec                      |76.6 usec                      |73.4 usec                      |77.6 usec                      |78.5 usec                      |148 usec                       |562.3x                                            |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |metomi-isodatetime              |1.22 msec                      |1.67 msec                      |1.6 msec                       |1.6 msec                       |1.76 msec                      |N/A                            |10604.3x                                          |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |moment                          |**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|N/A                            |1782198.3x                                        |
    +--------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+

ciso8601 takes 115 nsec, which is **1.7x faster than datetime (builtin)**, the next fastest Python 3.11 parser in this comparison.

.. </include:benchmark_with_time_zone.rst>

.. <include:benchmark_module_versions.rst>

Tested on Linux 5.15.49-linuxkit using the following modules:

.. code:: python

  aniso8601==9.0.1
  arrow==0.17.0 (on Python 2.7), arrow==1.2.3 (on Python 3.7, 3.8, 3.9, 3.10, 3.11)
  backports.datetime_fromisoformat==2.0.0
  ciso8601==2.3.0
  iso8601==0.1.16 (on Python 2.7), iso8601==1.1.0 (on Python 3.7, 3.8, 3.9, 3.10, 3.11)
  iso8601utils==0.1.2
  isodate==0.6.1
  maya==0.6.1
  metomi-isodatetime==1!3.0.0
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
