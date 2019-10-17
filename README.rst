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
Tested with Python 2.7, 3.4, 3.5, 3.6, 3.7, 3.8.

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

Parsing a timestamp with no time zone information (ex. ``2014-01-09T21:48:00``):

.. <include:benchmark_with_no_time_zone.rst>

.. table:: 

    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |    Module     |Python 3.8|Python 3.7|Python 3.6|Python 3.5|Python 3.4|          Python 2.7           |Relative Slowdown (versus ciso8601, Python 3.8)|
    +===============+==========+==========+==========+==========+==========+===============================+===============================================+
    |ciso8601       |201 nsec  |157 nsec  |160 nsec  |139 nsec  |148 nsec  |147 nsec                       |N/A                                            |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |pendulum       |215 nsec  |232 nsec  |234 nsec  |205 nsec  |192 nsec  |9.44 usec                      |1.1x                                           |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |udatetime      |906 nsec  |1.06 usec |767 nsec  |702 nsec  |819 nsec  |923 nsec                       |4.5x                                           |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |str2date       |5.96 usec |7.75 usec |7.27 usec |6.84 usec |7.6 usec  |**Incorrect Result** (``None``)|29.7x                                          |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |isodate        |10.3 usec |10 usec   |11.1 usec |11.9 usec |12.3 usec |43.6 usec                      |51.3x                                          |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |iso8601utils   |10.3 usec |8.63 usec |9.16 usec |10.3 usec |9.58 usec |11.1 usec                      |51.5x                                          |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |iso8601        |10.9 usec |11.1 usec |10.5 usec |11.2 usec |11.5 usec |25.6 usec                      |54.2x                                          |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |PySO8601       |13.9 usec |21.9 usec |20.2 usec |15.9 usec |23.7 usec |16.4 usec                      |69.4x                                          |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |aniso8601      |14.5 usec |15 usec   |15.8 usec |15.9 usec |16.1 usec |17.2 usec                      |72.5x                                          |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |zulu           |25.3 usec |29.9 usec |28.2 usec |27.4 usec |33 usec   |N/A                            |126.3x                                         |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |maya           |42.9 usec |57.4 usec |58.2 usec |67.5 usec |87.6 usec |100 usec                       |213.7x                                         |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |arrow          |85.7 usec |81.8 usec |75.7 usec |78.7 usec |N/A       |93.9 usec                      |427.1x                                         |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |python-dateutil|122 usec  |82.7 usec |72.2 usec |77.1 usec |74.4 usec |131 usec                       |609.5x                                         |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+
    |moment         |3.81 msec |4.46 msec |3.12 msec |3.66 msec |N/A       |3.59 msec                      |19011.9x                                       |
    +---------------+----------+----------+----------+----------+----------+-------------------------------+-----------------------------------------------+

ciso8601 takes 201 nsec, which is **1.1x faster than pendulum**, the next fastest ISO 8601 parser in this comparison.

.. </include:benchmark_with_no_time_zone.rst>

Parsing a timestamp with time zone information (ex. ``2014-01-09T21:48:00-05:30``):

.. <include:benchmark_with_time_zone.rst>

.. table:: 

    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |    Module     |          Python 3.8           |          Python 3.7           |          Python 3.6           |          Python 3.5           |Python 3.4|          Python 2.7           |Relative Slowdown (versus ciso8601, Python 3.8)|
    +===============+===============================+===============================+===============================+===============================+==========+===============================+===============================================+
    |ciso8601       |207 nsec                       |219 nsec                       |282 nsec                       |262 nsec                       |264 nsec  |360 nsec                       |N/A                                            |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |pendulum       |249 nsec                       |225 nsec                       |209 nsec                       |212 nsec                       |209 nsec  |12.9 usec                      |1.2x                                           |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |udatetime      |806 nsec                       |866 nsec                       |817 nsec                       |827 nsec                       |792 nsec  |835 nsec                       |3.9x                                           |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |str2date       |7.57 usec                      |10.7 usec                      |7.98 usec                      |8.48 usec                      |9.06 usec |**Incorrect Result** (``None``)|36.7x                                          |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |isodate        |12 usec                        |13.5 usec                      |14.7 usec                      |15.4 usec                      |18.8 usec |47.6 usec                      |58.3x                                          |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |iso8601        |12.8 usec                      |14.6 usec                      |14.6 usec                      |15.2 usec                      |17.7 usec |30 usec                        |61.8x                                          |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |aniso8601      |19.4 usec                      |30.4 usec                      |22.1 usec                      |20.5 usec                      |21.9 usec |20.1 usec                      |94.0x                                          |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |iso8601utils   |22.5 usec                      |25.3 usec                      |26.4 usec                      |25.7 usec                      |27 usec   |26.9 usec                      |108.9x                                         |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |zulu           |25.6 usec                      |31.2 usec                      |30 usec                        |32.3 usec                      |30.7 usec |N/A                            |124.1x                                         |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |PySO8601       |25.9 usec                      |35.4 usec                      |25.6 usec                      |29.5 usec                      |27.7 usec |25.7 usec                      |125.2x                                         |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |maya           |48.5 usec                      |46.6 usec                      |51.3 usec                      |63.2 usec                      |68.1 usec |125 usec                       |234.9x                                         |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |python-dateutil|79.3 usec                      |88.5 usec                      |101 usec                       |89.8 usec                      |91.9 usec |160 usec                       |384.2x                                         |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |arrow          |86.2 usec                      |95.2 usec                      |95 usec                        |101 usec                       |N/A       |103 usec                       |417.2x                                         |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+
    |moment         |**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|**Incorrect Result** (``None``)|N/A       |**Incorrect Result** (``None``)|3442935.3x                                     |
    +---------------+-------------------------------+-------------------------------+-------------------------------+-------------------------------+----------+-------------------------------+-----------------------------------------------+

ciso8601 takes 207 nsec, which is **1.2x faster than pendulum**, the next fastest ISO 8601 parser in this comparison.

.. </include:benchmark_with_time_zone.rst>

.. <include:benchmark_module_versions.rst>

Tested on Darwin 18.7.0 using the following modules:

.. code:: python

  aniso8601==8.0.0
  arrow==0.15.2
  ciso8601==2.1.2
  iso8601==0.1.12
  iso8601utils==0.1.2
  isodate==0.6.0
  maya==0.6.1
  moment==0.8.2
  pendulum==2.0.5
  PySO8601==0.2.0
  python-dateutil==2.8.0
  str2date==0.905
  udatetime==0.0.16
  zulu==1.1.1

.. </include:benchmark_module_versions.rst>

**Note:** ciso8601 doesn't support the entirety of the ISO 8601 spec, `only a popular subset`_.

For full benchmarking details (or to run the benchmark yourself), see `benchmarking/README.rst`_

.. _`benchmarking/README.rst`: https://github.com/closeio/ciso8601/blob/master/benchmarking/README.rst

Dependency on pytz (Python 2)
-----------------------------

In Python 2, ``ciso8601`` uses the `pytz`_ library while parsing timestamps with time zone information. This means that if you wish to parse such timestamps, you must first install ``pytz``:

.. _pytz: http://pytz.sourceforge.net/

.. code:: python
  
  pip install pytz

Otherwise, ``ciso8601`` will raise an exception when you try to parse a timestamp with time zone information:

.. code:: python
  
  In [2]: ciso8601.parse_datetime('2014-12-05T12:30:45.123456-05:30')
  Out[2]: ImportError: Cannot parse a timestamp with time zone information without the pytz dependency. Install it with `pip install pytz`.

``pytz`` is intentionally not an explicit dependency of ``ciso8601``. This is because many users use ``ciso8601`` to parse only naive timestamps, and therefore don't need this extra dependency.
In Python 3, ``ciso8601`` makes use of the built-in `datetime.timezone`_ class instead, so ``pytz`` is not necessary.

.. _datetime.timezone: https://docs.python.org/3/library/datetime.html#timezone-objects

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
