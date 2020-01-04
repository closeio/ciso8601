<!-- Generated with "Markdown T​O​C" extension for Visual Studio Code -->
<!-- TOC anchorMode:github.com -->

- [Unreleased](#unreleased)
- [2.x.x](#2xx)
  - [Version 2.1.3](#version-213)
  - [Version 2.1.2](#version-212)
  - [Version 2.1.1](#version-211)
  - [Version 2.1.0](#version-210)
  - [Version 2.0.1](#version-201)
  - [Version 2.0.0](#version-200)
    - [Breaking changes](#breaking-changes)
    - [Other Changes](#other-changes)
    - [v1.x.x -> 2.0.0 Migration guide](#v1xx---200-migration-guide)
      - [ValueError instead of None](#valueerror-instead-of-none)
      - [Tightened ISO 8601 conformance](#tightened-iso-8601-conformance)
      - [`parse_datetime_unaware` has been renamed](#parsedatetimeunaware-has-been-renamed)

<!-- /TOC -->

# Unreleased

* N/A

# 2.x.x

## Version 2.1.3

* Fixed a problem where non-ASCII characters would give bad error messages (#84). Thanks @olliemath.

## Version 2.1.2

* Fixed a problem where `ciso8601.__version__` was not working (#80). Thanks @ianhoffman.
* Added Python 3.8 support (#83)
* Added benchmarking scripts (#55)

## Version 2.1.1

* Fixed a problem where builds on Windows were not working (#76). Thanks @alexandrul and @gillesdouaire, and sorry.

## Version 2.1.0

* Added [Mypy](http://mypy-lang.org/)/[PEP 484](https://www.python.org/dev/peps/pep-0484/) typing information (#68, Thanks @NickG123).
* Added a new function: `parse_rfc3339`, which strictly parses RFC 3339 (#70).
* No longer accept mixed "basic" and "extended" format timestamps (#73).
    * ex. `20140203T23:35:27` and `2014-02-03T233527` are not valid in ISO 8601, but were not raising `ValueError`.
    * Attempting to parse such timestamps now raises `ValueError`

## Version 2.0.1

* Fixed some memory leaks introduced in 2.0.0 (#51)

## Version 2.0.0

Version 2.0.0 was a major rewrite of `ciso8601`.

Version 1.x.x had a problem with error handling in the case of invalid timestamps.

In 1.x.x, parse_datetime:

* All valid datetime strings within the supported subset of ISO 8601 would result in the correct Python datetime (this was good)
* Some invalid timestamps will return `None` and others might get truncated and return an incorrect Python datetime (this was bad)

A developer with a given timestamp string, could not predict a priori what `ciso8601` is going to return without looking at the code.
Fundamentally, this is the problem that version 2 addressed.

Fundamentally, `parse_datetime(dt: String): datetime` was rewritten so that it takes a string and either:

* Returns a properly parsed Python datetime, **if and only if** that **entire** string conforms to the supported subset of ISO 8601
* Raises an `ValueError` with a description of the reason why the string doesn't conform to the supported subset of ISO 8601

### Breaking changes

1. Version 2 now raises `ValueError` when a timestamp does not conform to the supported subset of ISO 8601
    * This includes trailing characters in the timestamp
    * No longer accepts single character "day" values
    * See migration guide below for more examples
2. `parse_datetime_unaware` was renamed to `parse_datetime_as_naive` (See "Migration Guide" below for reasons)

### Other Changes

* Attempting to parse a timestamp with time zone information without having pytz installed raises `ImportError` (Only affects Python 2.7). Fixes #19
* Added support for the special case of midnight (24:00:00) that is valid in ISO 8601. Fixes #41
* Fixed bug where "20140200" would not fail, but produce 2014-02-01. Fixes #42

### v1.x.x -> 2.0.0 Migration guide

#### ValueError instead of None

Places where you were checking for a return of `None` from ciso8601:

```python
    timestamp = "2018-01-01T00:00:00+05:00"
    dt = parse_datetime(timestamp)
    if dt is None:
        raise ValueError(f"Could not parse {timestamp}")
```

You should change to now expect `ValueError` to be thrown:

```python
    timestamp = "2018-01-01T00:00:00+05:00"
    dt = parse_datetime(timestamp)
```

#### Tightened ISO 8601 conformance

The rules with respect to what ciso8601 will consider a conforming ISO 8601 string have been tightened.

Now a timestamp will parse **if and only if** the timestamp is 100% conforming to the supported subset of the ISO 8601 specification.


```python
    # trailing separator
    "2014-"
    "2014-01-"
    "2014-01-01T"
    "2014-01-01T00:"
    "2014-01-01T00:00:"
    "2014-01-01T00:00:00-"
    "2014-01-01T00:00:00-00:"

    # Mix of no-separator and separator
    "201401-02"
    "2014-0102"
    "2014-01-02T00:0000"
    "2014-01-02T0000:00"

    "2014-01-02T01:23:45Zabcdefghij" # Trailing characters

    "2014-01-1" # Single digit day
    "2014-01-01T00:00:00-0:04" # Single digit tzhour
    "2014-01-01T00:00:00-00:4" # Single digit tzminute
```

These should have been considered bugs in ciso8601 1.x.x, but it may be the case that your code was relying on the previously lax parsing rules.

#### `parse_datetime_unaware` has been renamed

`parse_datetime_unaware` existed for the case where your input timestamp had time zone information, but you wanted to ignore the time zone information and therefore could save some cycles by not creating the underlying `tzinfo` object.

It has been renamed to `parse_datetime_as_naive` for 2 reasons:

1. Developers were assuming that `parse_datetime_unaware` was the function to use for parsing naive timestamps, when really it is for parsing timestamps with time zone information as naive datetimes. `parse_datetime` handles parsing both timestamps with and without time zone information and should be used for all parsing, unless you actually need this use case. See additional description in [the README](https://github.com/closeio/ciso8601/tree/raise-valueerror-on-invalid-dates#ignoring-timezone-information-while-parsing) for a more detailed description of this use case.
2. Python [refers to datetimes without time zone information](https://docs.python.org/3/library/datetime.html) as `naive`, not `unaware`

Before switching all instances of `parse_datetime_unaware`, make sure to ask yourself whether you actually intended to use `parse_datetime_unaware`.

* If you meant to parse naive timestamps as naive datetimes, use `parse_datetime` instead.
* If you actually meant to parse **timestamps with time zone information** as **naive** datetimes, use `parse_datetime_as_naive` instead.

|                                    | Input with TZ Info | Input without TZ Info |
| ---------------------------------- | ------------------ | --------------------- |
| `parse_datetime()` output          | tz aware datetime  | tz naive datetime     |
| `parse_datetime_as_naive()` output | tz naive datetime  | tz naive datetime     |
