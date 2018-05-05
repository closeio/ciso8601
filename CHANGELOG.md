# Version 2.0

This was a major rewrite of `ciso8601`.

Fundamentally, `parse_datetime(dt: String): datetime` was rewritten so that it takes a string and either:

   * Returns a properly parsed Python datetime, **if and only if** that **entire** string conforms to the supported subset of ISO 8601
   * Raise an Exception (ex. `ValueError`) with a description of the reason why the string doesn't conform to ISO 8601

This is a departure from the past where `ciso8601` would sometimes return `None` and sometimes return a malformed `datetime`, depending on the nature of your data quality problem.

## Breaking changes:

1. No longer allows you to parse a tz-aware timestamp as tz-naive datetime
    * In fact, `parse_datetime_unaware` doesn't even exist anymore).
1. Throws exception when a timestamp does not conform to ISO 8601
    * This includes trailing characters in the timestamp
    * No longer accepts single character "day" values
    * See migration guide below for more examples

## v1.x -> 2.0 Migration guide

### `parse_datetime_unaware` has been removed

`parse_datetime_unaware` existed for the case where your input had `tzinfo`, but you wanted to ignore the tzinfo and therefore could save some cycles by not parsing the tzinfo characters.

The use case was deemed not compelling enough. Ignoring tzinfo on a tz-aware timestamp is almost never what you want to do. If you still want to ignore tzinfo, just use `parse_datetime` and then replace the tzinfo manually:

```python
    dt = parse_datetime("2018-01-01T00:00:00+05:00").replace(tzinfo=None)
```

`parse_datetime` now handles both tz-aware and tz-naive timestamps. Instances where you were using `parse_datetime_unaware` to parse tz-naive timestamps, you can simply use `parse_datetime` instead.

```python
    dt = parse_datetime("2018-01-01T00:00:00")
```

### ValueError instead of None

Places where you were checking for a return of `None` from ciso8601:

```python
    timestamp = "2018-01-01T00:00:00+05:00"
    dt = parse_datetime(timestamp)
    if dt is None:
        raise ValueError(f"Could not parse {timestamp}")
```

You should change to now expect ValueError to be thrown:

```python
    timestamp = "2018-01-01T00:00:00+05:00"
    dt = parse_datetime(timestamp)
```

### Tightened ISO 8601 conformance

The rules with respect to what `ciso8601` will consider a conforming ISO 8601 string have been tightened.

Now a timestamp will parse **if and only if** the timestamp is 100% conforming to the supported subset of the ISO 8601 specification.


```python
    "2014-" # Missing the month
    "2014-01-" # trailing separator

    # Mix of no-separator and separator
    "201401-02" 
    "2014-0102"
    "2014-01-02T00:0000" 
    "2014-01-02T0000:00"
    
    "2014-01-02T01:23:45Zabcdefghij" # Trailing characters

    "2014-01-1" # Single digit day
```

These could have been considered bugs, but it may be the case that your code was relying on the previously lax parsing rules.