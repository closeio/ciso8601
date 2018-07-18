========
ciso8601
========

.. image:: https://img.shields.io/circleci/project/github/closeio/ciso8601.svg
    :target: https://circleci.com/gh/closeio/ciso8601/tree/master

.. image:: https://img.shields.io/pypi/v/ciso8601.svg
    :target: https://pypi.org/project/ciso8601/

.. image:: https://img.shields.io/pypi/pyversions/ciso8601.svg
    :target: https://pypi.org/project/ciso8601/
    
.. image:: https://img.shields.io/badge/Semantic%20Versioning%3F-%E2%9C%85-green.svg
    :target: https://semver.org/

``ciso8601`` converts `ISO 8601`_ date time strings into Python datetime objects.
Since it's written as a C module, it is much faster than other Python libraries.
Tested with Python 2.7, 3.4, 3.5, 3.6, 3.7b.

.. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601

(Interested in working on projects like this? `Close.io`_ is looking for `great engineers`_ to join our team)

.. _Close.io: https://close.io
.. _great engineers: https://jobs.close.io


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

Date time string with no time zone information:

.. code:: python

  In [1]: import datetime, aniso8601, iso8601, isodate, dateutil.parser, arrow, ciso8601

  In [2]: ds = u'2014-01-09T21:48:00.921000'

  In [3]: %timeit ciso8601.parse_datetime(ds)
  1000000 loops, best of 3: 204 ns per loop

  In [4]: %timeit datetime.datetime.strptime(ds, "%Y-%m-%dT%H:%M:%S.%f")
  100000 loops, best of 3: 15 µs per loop

  In [5]: %timeit dateutil.parser.parse(ds)
  10000 loops, best of 3: 122 µs per loop

  In [6]: %timeit aniso8601.parse_datetime(ds)
  10000 loops, best of 3: 28.9 µs per loop

  In [7]: %timeit iso8601.parse_date(ds)
  10000 loops, best of 3: 42 µs per loop

  In [8]: %timeit isodate.parse_datetime(ds)
  10000 loops, best of 3: 69.4 µs per loop

  In [9]: %timeit arrow.get(ds).datetime
  10000 loops, best of 3: 87 µs per loop

ciso8601 takes 0.204us, which is 73x faster than datetime's strptime, which is
not a full ISO8601 parser. It is **141x faster than aniso8601**, the next fastest
ISO8601 parser in this comparison.

Date time string with time zone information:

.. code:: python

  In [1]: import datetime, aniso8601, iso8601, isodate, dateutil.parser, arrow, ciso8601

  In [2]: ds = u'2014-01-09T21:48:00.921000+05:30'

  In [3]: %timeit ciso8601.parse_datetime(ds)
  1000000 loops, best of 3: 525 ns per loop

  In [4]: %timeit dateutil.parser.parse(ds)
  10000 loops, best of 3: 162 µs per loop

  In [5]: %timeit aniso8601.parse_datetime(ds)
  10000 loops, best of 3: 36.8 µs per loop

  In [6]: %timeit iso8601.parse_date(ds)
  10000 loops, best of 3: 53.5 µs per loop

  In [7]: %timeit isodate.parse_datetime(ds)
  10000 loops, best of 3: 82.6 µs per loop

  In [8]: %timeit arrow.get(ds).datetime
  10000 loops, best of 3: 104 µs per loop

Even with time zone information, ``ciso8601`` is 70x as fast as ``aniso8601``.

Tested on Python 2.7.10 on macOS 10.12.6 using the following modules:

.. code:: python

  aniso8601==1.2.1
  arrow==0.10.0
  ciso8601==1.0.4
  iso8601==0.1.12
  isodate==0.5.4
  python-dateutil==2.6.1

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
In Python 3, ``ciso8601`` makes use of the built-in `datetime.timezone`_ class instead, so pytz is not necessary.

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

Consistent with `RFC 3339`_, ``ciso860`` also allows either a space character, or a lower-case ``t``, to be used instead of a ``T``.

.. _RFC 3339: https://stackoverflow.com/questions/522251/whats-the-difference-between-iso-8601-and-rfc-3339-date-formats)

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

Other Nice Features
-------------------

* `Semantic Versioning`_

.. _Semantic Versioning: https://semver.org

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
