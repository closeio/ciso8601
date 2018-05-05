========
ciso8601
========

.. image:: https://circleci.com/gh/closeio/ciso8601/tree/master.svg?style=svg&circle-token=72fc522063916cb1c6c5c9882b97db9d2ed651d8
    :target: https://circleci.com/gh/closeio/ciso8601/tree/master

``ciso8601`` converts ISO8601 date time strings into Python datetime objects.
Since it's written as a C module, it is much faster than other Python libraries.
Tested with Python 2.7, 3.4, 3.5, 3.6.


(Interested in working on projects like this? `Close.io`_ is looking for `great engineers`_ to join our team)

.. _Close.io: http://close.io
.. _great engineers: http://jobs.close.io


.. contents:: Contents


Usage
-----

.. code:: bash

  % pip install ciso8601

.. code:: python

  In [1]: import ciso8601

  In [2]: ciso8601.parse_datetime('2014-12-05T12:30:45.123456-05:30')
  Out[2]: datetime.datetime(2014, 12, 5, 12, 30, 45, 123456, tzinfo=pytz.FixedOffset(330))

  In [3]: ciso8601.parse_datetime('20141205T123045')
  Out[3]: datetime.datetime(2014, 12, 5, 12, 30, 45)

If time zone information is provided, an aware datetime object will be returned.
Otherwise, the datetime is unaware. Please note that it takes more time to parse
aware datetimes, especially if they're not in UTC.

If parsing fails, an Exception will be raised (typically `ValueError`). The parser will attempt to parse as
much of the date time as possible.

Migration to v2
---------------

Version 2.0.0 of ``ciso8601`` changed the core implementation. This was not entirely backwards compatible, and care should be taken when migrating
See `CHANGELOG`_ for details.

.. _CHANGELOG: https://github.com/closeio/ciso8601/blob/master/CHANGELOG.md

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

Supported Subset
-----------------

ciso8601 only supports a subset of ISO 8601.

Calendar Dates
^^^^^^^^^^^^^^

The following calendar date formats are supported:

.. table:: Supported date formats
   :widths: auto
============== ============== ==================
Format         Example        Supported
============== ============== ==================
``YYYY-MM-DD`` ``2018-04-29`` ✅
``YYYY-MM``    ``2018-04``    ✅
``YYYYMMDD``   ``2018-04``    ✅
``--MM-DD``    ``--04-29``    ❌              
``--MMDD``     ``--0429``     ❌              
============== ============== ==================

Times
^^^^^

Times are optional and are separated from the date by the letter ``T``.
``ciso860`` extends the ISO 8601 specification slightly by allowing a space character to be used instead of a ``T``.

The following time formats are supported:

.. table:: Supported time formats
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
Midnight (special case)             ``24:00:00``        ❌               
``hh.hhh`` (fractional hours)       ``11.5``            ❌               
``hh:mm.mmm`` (fractional minutes)  ``11:30.5``         ❌               
=================================== =================== ============== 

**Note:** Python datetime objects only have microsecond precision (6 digits). Any additional precision will be truncated.
If you need greater precision than microsecond precision, please do not use `ciso8601`.

Time Zone Information
^^^^^^^^^^^^^^^^^^^^^

Time zone information may be provided in one of the following formats:

.. table:: Supported time zone formats
   :widths: auto
========== ========== =========== 
Format     Example    Supported          
========== ========== =========== 
``Z``      ``Z``      ✅
``±hh``    ``+11``    ✅
``±hhmm``  ``+1130``  ✅
``±hh:mm`` ``+11:30`` ✅
========== ========== ===========