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
Tested with cPython 2.7, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10.

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

    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |    Module     |Python 3.10|Python 3.9|Python 3.8|Python 3.7|Python 3.6|Python 3.5|          Python 2.7           |Relative Slowdown (versus ciso8601, latest Python)|
    +===============+===========+==========+==========+==========+==========+==========+===============================+==================================================+
    |ciso8601       |151 nsec   |135 nsec  |165 nsec  |135 nsec  |131 nsec  |154 nsec  |168 nsec                       |N/A                                               |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |pendulum       |166 nsec   |155 nsec  |185 nsec  |175 nsec  |156 nsec  |166 nsec  |7.89 usec                      |1.1x                                              |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |udatetime      |N/A        |N/A       |763 nsec  |762 nsec  |784 nsec  |782 nsec  |696 nsec                       |4.6x                                              |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |str2date       |6.03 usec  |6.1 usec  |5.84 usec |6.59 usec |6.49 usec |8.97 usec |**Incorrect Result** (``None``)|39.9x                                             |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |iso8601utils   |N/A        |8.26 usec |8.28 usec |9.28 usec |N/A       |12.2 usec |10.7 usec                      |61.0x                                             |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |iso8601        |8.54 usec  |8.72 usec |8.7 usec  |9.95 usec |10.1 usec |13.2 usec |24.8 usec                      |56.5x                                             |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |isodate        |9.14 usec  |9.33 usec |9.3 usec  |10.5 usec |11 usec   |13.6 usec |45.4 usec                      |60.4x                                             |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |PySO8601       |15.9 usec  |15.7 usec |15.2 usec |16.3 usec |16.8 usec |20.3 usec |17 usec                        |105.0x                                            |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |zulu           |23.2 usec  |23.1 usec |21.3 usec |24.9 usec |27.8 usec |N/A       |N/A                            |153.6x                                            |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |aniso8601      |23.6 usec  |25.1 usec |23.8 usec |28.6 usec |29.6 usec |35.5 usec |31.3 usec                      |155.9x                                            |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |maya           |48 usec    |48.5 usec |48.4 usec |50.1 usec |57.3 usec |77.7 usec |69.8 usec                      |317.3x                                            |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |python-dateutil|64.7 usec  |67.8 usec |62.2 usec |73.6 usec |77.8 usec |98.8 usec |135 usec                       |427.6x                                            |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |arrow          |71.8 usec  |69.7 usec |67.3 usec |78.1 usec |76.9 usec |97.5 usec |87.5 usec                      |474.6x                                            |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |moment         |1.41 msec  |1.4 msec  |1.35 msec |1.57 msec |1.45 msec |1.79 msec |2.32 msec                      |9338.4x                                           |
    +---------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+

ciso8601 takes 151 nsec, which is **1.1x faster than pendulum**, the next fastest ISO 8601 parser in this comparison.

.. </include:benchmark_with_no_time_zone.rst>

Parsing a timestamp with time zone information (e.g., ``2014-01-09T21:48:00-05:30``):

.. <include:benchmark_with_time_zone.rst>

.. table::

    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |    Module     |          Python 3.10          |          Python 3.9           |          Python 3.8           |          Python 3.7           |          Python 3.6           |          Python 3.5           |          Python 2.7           |Relative Slowdown (versus ciso8601, latest Python)|
    +===============+===============================+===============================+===============================+===============================+===============================+===============================+===============================+==================================================+
    |ciso8601       |166 nsec                       |147 nsec                       |177 nsec                       |156 nsec                       |144 nsec                       |159 nsec                       |193 nsec                       |N/A                                               |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |pendulum       |189 nsec                       |178 nsec                       |216 nsec                       |186 nsec                       |171 nsec                       |183 nsec                       |12.6 usec                      |1.1x                                              |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |udatetime      |N/A                            |N/A                            |961 nsec                       |944 nsec                       |959 nsec                       |981 nsec                       |902 nsec                       |5.4x                                              |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |str2date       |7.5 usec                       |7.8 usec                       |7.51 usec                      |8.12 usec                      |8.06 usec                      |11.1 usec                      |**Incorrect Result** (``None``)|45.3x                                             |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |iso8601        |12.3 usec                      |12.7 usec                      |12.2 usec                      |13.6 usec                      |14.1 usec                      |18.7 usec                      |30.4 usec                      |74.5x                                             |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |isodate        |12.5 usec                      |12.9 usec                      |12.2 usec                      |14 usec                        |14.7 usec                      |18.7 usec                      |48.6 usec                      |75.6x                                             |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |iso8601utils   |N/A                            |23.1 usec                      |21.8 usec                      |26.2 usec                      |N/A                            |34.5 usec                      |27.8 usec                      |157.8x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |PySO8601       |24.3 usec                      |24.6 usec                      |22.7 usec                      |25.3 usec                      |26.1 usec                      |31.7 usec                      |26.4 usec                      |146.8x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |zulu           |27 usec                        |27.1 usec                      |25.6 usec                      |27.6 usec                      |32.1 usec                      |N/A                            |N/A                            |162.9x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |aniso8601      |33.2 usec                      |34.6 usec                      |32.8 usec                      |40.1 usec                      |40.1 usec                      |48.7 usec                      |43.6 usec                      |200.4x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |maya           |49.5 usec                      |48.5 usec                      |46.3 usec                      |49.8 usec                      |58.7 usec                      |79.1 usec                      |75.6 usec                      |299.0x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |python-dateutil|81.4 usec                      |85.5 usec                      |81.7 usec                      |95.7 usec                      |101 usec                       |126 usec                       |165 usec                       |491.3x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |arrow          |83.5 usec                      |82.6 usec                      |81.2 usec                      |93.4 usec                      |90.4 usec                      |118 usec                       |108 usec                       |504.4x                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |moment         |**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|1110684.9x                                        |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+

ciso8601 takes 166 nsec, which is **1.1x faster than pendulum**, the next fastest ISO 8601 parser in this comparison.

.. </include:benchmark_with_time_zone.rst>

.. <include:benchmark_module_versions.rst>

Tested on Linux 5.10.16.3-microsoft-standard-WSL2 using the following modules:

.. code:: python

  aniso8601==9.0.1
  arrow==0.17.0 (on Python 2.7, 3.5), arrow==1.2.0 (on Python 3.10, 3.6, 3.7, 3.8, 3.9)
  ciso8601==2.2.0
  iso8601==0.1.16
  iso8601utils==0.1.2
  isodate==0.6.0
  maya==0.6.1
  moment==0.12.1
  pendulum==2.1.2
  PySO8601==0.2.0
  python-dateutil==2.8.2
  str2date==0.905
  udatetime==0.0.16
  zulu==2.0.0

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
