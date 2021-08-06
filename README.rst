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
Tested with cPython 2.7, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9.

**Note:** ciso8601 doesn't support the entirety of the ISO 8601 spec, `only a popular subset`_.

.. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601
.. _RFC 3339: https://tools.ietf.org/html/rfc3339

.. _`only a popular subset`: https://github.com/closeio/ciso8601#supported-subset-of-iso-8601

(Interested in working on projects like this? `Close`_ is looking for `great engineers`_ to join our team)

.. _Close: https://close.com
.. _great engineers: https://jobs.close.com


.. contents:: Contents


Quick Start
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

Error Handling
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

    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |    Module     |Python 3.9|Python 3.8|Python 3.7|Python 3.6|Python 3.5|          Python 2.7           |Relative Slowdown (versus ciso8601, latest Python)|
    +===============+==========+==========+==========+==========+==========+===============================+==================================================+
    |ciso8601       |154 nsec  |168 nsec  |166 nsec  |157 nsec  |153 nsec  |171 nsec                       |N/A                                               |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |pendulum       |181 nsec  |195 nsec  |188 nsec  |180 nsec  |181 nsec  |9.8 usec                       |1.2x                                              |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |udatetime      |N/A       |697 nsec  |663 nsec  |676 nsec  |667 nsec  |677 nsec                       |4.1x                                              |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |str2date       |6.12 usec |6.56 usec |7.41 usec |7.43 usec |9.04 usec |**Incorrect Result** (``None``)|39.8x                                             |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |iso8601utils   |8.27 usec |8.68 usec |9.72 usec |N/A       |11.8 usec |11.5 usec                      |53.8x                                             |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |isodate        |9.18 usec |9.74 usec |11.3 usec |11.8 usec |13.7 usec |42.2 usec                      |59.6x                                             |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |iso8601        |9.42 usec |10.1 usec |11.7 usec |12 usec   |13.5 usec |27.4 usec                      |61.2x                                             |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |PySO8601       |15.9 usec |15.8 usec |18 usec   |17.9 usec |19.3 usec |17 usec                        |103.1x                                            |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |aniso8601      |21.1 usec |22.3 usec |27.9 usec |29.6 usec |31.2 usec |32.5 usec                      |137.3x                                            |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |zulu           |22.5 usec |23.2 usec |25.2 usec |28.1 usec |N/A       |N/A                            |146.6x                                            |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |maya           |40.9 usec |40.8 usec |46.3 usec |53.6 usec |67.5 usec |63.2 usec                      |265.6x                                            |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |python-dateutil|60.4 usec |61 usec   |70.4 usec |76.5 usec |85.1 usec |124 usec                       |392.9x                                            |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |arrow          |68.1 usec |66.2 usec |74.1 usec |73 usec   |84.9 usec |85.1 usec                      |442.8x                                            |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |moment         |1.44 msec |1.49 msec |1.66 msec |1.54 msec |1.82 msec |2.46 msec                      |9380.7x                                           |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+

ciso8601 takes 154 nsec, which is **1.2x faster than pendulum**, the next fastest ISO 8601 parser in this comparison.

.. </include:benchmark_with_no_time_zone.rst>

Parsing a timestamp with time zone information (e.g., ``2014-01-09T21:48:00-05:30``):

.. <include:benchmark_with_time_zone.rst>

.. table::

    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |    Module     |          Python 3.9           |          Python 3.8           |          Python 3.7           |          Python 3.6           |          Python 3.5           |          Python 2.7           |Relative Slowdown (versus ciso8601, latest Python)|
    +===============+===============================+===============================+===============================+===============================+===============================+===============================+==================================================+
    |ciso8601       |175 nsec                       |181 nsec                       |172 nsec                       |161 nsec                       |161 nsec                       |185 nsec                       |N/A                                               |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |pendulum       |207 nsec                       |228 nsec                       |209 nsec                       |205 nsec                       |201 nsec                       |15 usec                        |1.2x                                              |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |udatetime      |N/A                            |801 nsec                       |757 nsec                       |771 nsec                       |766 nsec                       |725 nsec                       |4.4x                                              |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |str2date       |7.97 usec                      |8.75 usec                      |8.22 usec                      |9.6 usec                       |11.7 usec                      |**Incorrect Result** (``None``)|45.6x                                             |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |iso8601        |12.7 usec                      |13.3 usec                      |16.6 usec                      |15.6 usec                      |17.8 usec                      |32.7 usec                      |72.5x                                             |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |isodate        |12.7 usec                      |13.3 usec                      |14.6 usec                      |15.7 usec                      |18.3 usec                      |46.5 usec                      |72.6x                                             |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |PySO8601       |23.3 usec                      |23.5 usec                      |26.2 usec                      |26.6 usec                      |30.5 usec                      |26.5 usec                      |133.5x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |iso8601utils   |23.7 usec                      |22.9 usec                      |25.5 usec                      |N/A                            |31.2 usec                      |29.2 usec                      |135.7x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |zulu           |25.3 usec                      |24.6 usec                      |27.8 usec                      |31.7 usec                      |N/A                            |N/A                            |144.9x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |aniso8601      |28.3 usec                      |30.4 usec                      |35.3 usec                      |37.6 usec                      |42 usec                        |40.4 usec                      |162.1x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |maya           |42.4 usec                      |41.3 usec                      |45.9 usec                      |51.3 usec                      |66.8 usec                      |70.2 usec                      |242.6x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |arrow          |75.1 usec                      |73.2 usec                      |84.2 usec                      |83.5 usec                      |104 usec                       |101 usec                       |429.8x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |python-dateutil|76.9 usec                      |77.7 usec                      |85.4 usec                      |96 usec                        |108 usec                       |152 usec                       |440.2x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |moment         |**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|1134883.0x                                        |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+

ciso8601 takes 175 nsec, which is **1.2x faster than pendulum**, the next fastest ISO 8601 parser in this comparison.

.. </include:benchmark_with_time_zone.rst>

.. <include:benchmark_module_versions.rst>

Tested on Linux 5.10.25-linuxkit using the following modules:

.. code:: python

  aniso8601==9.0.1
  arrow==0.17.0 (on Python 2.7, 3.5), arrow==1.1.1 (on Python 3.6, 3.7, 3.8, 3.9)
  ciso8601==2.2.0
  iso8601==0.1.14
  iso8601utils==0.1.2
  isodate==0.6.0
  maya==0.6.1
  moment==0.12.1
  pendulum==2.1.2
  PySO8601==0.2.0
  python-dateutil==2.8.1
  str2date==0.905
  udatetime==0.0.16
  zulu==1.3.0

.. </include:benchmark_module_versions.rst>

**Note:** ciso8601 doesn't support the entirety of the ISO 8601 spec, `only a popular subset`_.

For full benchmarking details (or to run the benchmark yourself), see `benchmarking/README.rst`_

.. _`benchmarking/README.rst`: https://github.com/closeio/ciso8601/blob/master/benchmarking/README.rst

Supported Subset of ISO 8601
----------------------------

``ciso8601`` only supports the most common subset of ISO 8601.

Date Formats
^^^^^^^^^^^^

The following date formats are supported:

.. table::
   :widths: auto

   ============================= ============== ==================
   Format                        Example        Supported
   ============================= ============== ==================
   ``YYYY-MM-DD``                ``2018-04-29`` ✅
   ``YYYY-MM``                   ``2018-04``    ✅
   ``YYYYMMDD``                  ``2018-04``    ✅
   ``--MM-DD`` (omitted year)    ``--04-29``    ❌
   ``--MMDD`` (omitted year)     ``--0429``     ❌
   ``±YYYYY-MM`` (>4 digit year) ``+10000-04``  ❌
   ``+YYYY-MM`` (leading +)      ``+2018-04``   ❌
   ``-YYYY-MM`` (negative -)     ``-2018-04``   ❌
   ============================= ============== ==================

Week dates or ordinal dates are not currently supported.

.. table::
   :widths: auto

   ============================= ============== ==================
   Format                        Example        Supported
   ============================= ============== ==================
   ``YYYY-Www`` (week date)      ``2009-W01``   ❌
   ``YYYYWww`` (week date)       ``2009W01``    ❌
   ``YYYY-Www-D`` (week date)    ``2009-W01-1`` ❌
   ``YYYYWwwD`` (week date)      ``2009-W01-1`` ❌
   ``YYYY-DDD`` (ordinal date)   ``1981-095``   ❌
   ``YYYYDDD`` (ordinal date)    ``1981095``    ❌
   ============================= ============== ==================

Time Formats
^^^^^^^^^^^^

Times are optional and are separated from the date by the letter ``T``.

Consistent with `RFC 3339`__, ``ciso860`` also allows either a space character, or a lower-case ``t``, to be used instead of a ``T``.

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

Time Zone Information
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

Consistent with `RFC 3339`_, ``ciso860`` also allows a lower-case ``z`` to be used instead of a ``Z``.

Strict RFC 3339 Parsing
-----------------------

``ciso8601`` parses ISO 8601 datetimes, which can be thought of as a superset of `RFC 3339`_ (`roughly`_). In cases where you might want strict RFC 3339 parsing, ``ciso8601`` offers a ``parse_rfc3339`` method, which behaves in a similar manner to ``parse_datetime``:

.. _roughly: https://stackoverflow.com/questions/522251/whats-the-difference-between-iso-8601-and-rfc-3339-date-formats

``parse_rfc3339(dt: String): datetime`` is a function that takes a string and either:

* Returns a properly parsed Python datetime, **if and only if** the **entire** string conforms to RFC 3339.
* Raises a ``ValueError`` with a description of the reason why the string doesn't conform to RFC 3339.

Ignoring Timezone Information While Parsing
-------------------------------------------

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
