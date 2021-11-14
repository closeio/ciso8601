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

    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |      Module      |Python 3.10|Python 3.9|Python 3.8|Python 3.7|Python 3.6|Python 3.5|          Python 2.7           |Relative Slowdown (versus ciso8601, latest Python)|
    +==================+===========+==========+==========+==========+==========+==========+===============================+==================================================+
    |ciso8601          |147 nsec   |135 nsec  |150 nsec  |143 nsec  |131 nsec  |155 nsec  |159 nsec                       |N/A                                               |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |pendulum          |162 nsec   |151 nsec  |166 nsec  |162 nsec  |172 nsec  |176 nsec  |7.77 usec                      |1.1x                                              |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |udatetime         |N/A        |N/A       |724 nsec  |737 nsec  |731 nsec  |751 nsec  |678 nsec                       |4.8x                                              |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |str2date          |5.91 usec  |6.06 usec |5.17 usec |6.2 usec  |6.49 usec |9.05 usec |**Incorrect Result** (``None``)|40.1x                                             |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |iso8601           |7.99 usec  |8.16 usec |7.32 usec |8.74 usec |8.92 usec |12.7 usec |25 usec                        |54.2x                                             |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |iso8601utils      |N/A        |8 usec    |7.87 usec |9.02 usec |N/A       |12.5 usec |10.9 usec                      |59.3x                                             |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |isodate           |8.76 usec  |9.49 usec |8.78 usec |10.3 usec |10.8 usec |13.6 usec |44.1 usec                      |59.4x                                             |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |PySO8601          |14.9 usec  |15.4 usec |14.2 usec |16 usec   |16.3 usec |19.8 usec |16.7 usec                      |101.2x                                            |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |zulu              |21.9 usec  |21.6 usec |20.1 usec |22.9 usec |25 usec   |N/A       |N/A                            |148.2x                                            |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |aniso8601         |23.9 usec  |24.2 usec |22.5 usec |28 usec   |29.7 usec |34.6 usec |30.3 usec                      |161.8x                                            |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |maya              |47.8 usec  |47.8 usec |43.6 usec |47.6 usec |55.6 usec |77.1 usec |68.2 usec                      |324.1x                                            |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |python-dateutil   |62.3 usec  |65.9 usec |58 usec   |73.2 usec |76.3 usec |96.2 usec |132 usec                       |422.3x                                            |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |arrow             |71.6 usec  |67 usec   |65.4 usec |75 usec   |73.9 usec |96.2 usec |83.6 usec                      |485.4x                                            |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |moment            |1.43 msec  |1.4 msec  |1.3 msec  |1.56 msec |1.39 msec |1.78 msec |2.26 msec                      |9666.4x                                           |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+
    |metomi-isodatetime|1.72 msec  |1.64 msec |1.63 msec |2.02 msec |1.77 msec |2.15 msec |N/A                            |11674.2x                                          |
    +------------------+-----------+----------+----------+----------+----------+----------+-------------------------------+--------------------------------------------------+

ciso8601 takes 147 nsec, which is **1.1x faster than pendulum**, the next fastest ISO 8601 parser in this comparison.

.. </include:benchmark_with_no_time_zone.rst>

Parsing a timestamp with time zone information (e.g., ``2014-01-09T21:48:00-05:30``):

.. <include:benchmark_with_time_zone.rst>

.. table::

    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |      Module      |          Python 3.10          |          Python 3.9           |          Python 3.8           |          Python 3.7           |          Python 3.6           |          Python 3.5           |          Python 2.7           |Relative Slowdown (versus ciso8601, latest Python)|
    +==================+===============================+===============================+===============================+===============================+===============================+===============================+===============================+==================================================+
    |ciso8601          |159 nsec                       |143 nsec                       |156 nsec                       |149 nsec                       |142 nsec                       |154 nsec                       |190 nsec                       |N/A                                               |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |pendulum          |193 nsec                       |181 nsec                       |201 nsec                       |183 nsec                       |172 nsec                       |191 nsec                       |12.6 usec                      |1.2x                                              |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |udatetime         |N/A                            |N/A                            |907 nsec                       |947 nsec                       |953 nsec                       |986 nsec                       |892 nsec                       |5.8x                                              |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |str2date          |7.5 usec                       |7.76 usec                      |6.92 usec                      |7.77 usec                      |7.98 usec                      |10.7 usec                      |**Incorrect Result** (``None``)|47.0x                                             |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |iso8601           |12.4 usec                      |12.4 usec                      |11.2 usec                      |12.4 usec                      |12.7 usec                      |18.8 usec                      |30.5 usec                      |77.9x                                             |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |isodate           |12.7 usec                      |12.9 usec                      |11.5 usec                      |13.7 usec                      |14.5 usec                      |18.2 usec                      |48.8 usec                      |79.8x                                             |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |iso8601utils      |N/A                            |22.2 usec                      |21 usec                        |25.6 usec                      |N/A                            |34.2 usec                      |28.1 usec                      |155.3x                                            |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |PySO8601          |24.4 usec                      |24.9 usec                      |21.7 usec                      |24.9 usec                      |25.3 usec                      |30.9 usec                      |26.3 usec                      |153.0x                                            |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |zulu              |25.9 usec                      |25.5 usec                      |24.1 usec                      |26.7 usec                      |30.5 usec                      |N/A                            |N/A                            |162.3x                                            |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |aniso8601         |32.9 usec                      |35.1 usec                      |32.6 usec                      |40 usec                        |40.7 usec                      |47.7 usec                      |42.1 usec                      |206.6x                                            |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |maya              |50.9 usec                      |49.7 usec                      |44.1 usec                      |50.5 usec                      |58.4 usec                      |78.8 usec                      |76.2 usec                      |319.2x                                            |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |arrow             |83.3 usec                      |84.3 usec                      |79 usec                        |92.9 usec                      |89.3 usec                      |116 usec                       |109 usec                       |522.0x                                            |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |python-dateutil   |83.8 usec                      |86 usec                        |81.1 usec                      |94.3 usec                      |97 usec                        |126 usec                       |161 usec                       |525.2x                                            |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |metomi-isodatetime|1.77 msec                      |1.76 msec                      |1.63 msec                      |2.06 msec                      |1.81 msec                      |2.31 msec                      |N/A                            |11128.2x                                          |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+
    |moment            |**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|1126277.5x                                        |
    +------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+--------------------------------------------------+

ciso8601 takes 159 nsec, which is **1.2x faster than pendulum**, the next fastest ISO 8601 parser in this comparison.

.. </include:benchmark_with_time_zone.rst>

.. <include:benchmark_module_versions.rst>

Tested on Linux 5.10.16.3-microsoft-standard-WSL2 using the following modules:

.. code:: python

  aniso8601==9.0.1
  arrow==0.17.0 (on Python 2.7, 3.5), arrow==1.2.1 (on Python 3.10, 3.6, 3.7, 3.8, 3.9)
  ciso8601==2.2.0
  iso8601==0.1.16 (on Python 2.7, 3.5), iso8601==1.0.0 (on Python 3.10, 3.6, 3.7, 3.8, 3.9)
  iso8601utils==0.1.2
  isodate==0.6.0
  maya==0.6.1
  metomi-isodatetime==1!2.0.2
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
