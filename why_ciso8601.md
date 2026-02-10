# Should I use ciso8601? <!-- omit in toc -->

`ciso8601`'s goal is to be the world's fastest ISO 8601 datetime parser for Python.
However, `ciso8601` is not the right choice for all use cases.
This document aims to describe some considerations to make when choosing a timestamp parsing library.

- [Do you care about the performance of timestamp parsing?](#do-you-care-about-the-performance-of-timestamp-parsing)
- [Do you need strict RFC 3339 parsing?](#do-you-need-strict-rfc-3339-parsing)
- [Do you need to support Python \< 3.11?](#do-you-need-to-support-python--311)
- [Do you need to support Python \< 3.8?](#do-you-need-to-support-python--38)

### Flowchart <!-- omit in toc -->

```mermaid
graph TD;
    A[Do you care about the performance of timestamp parsing?]
    A--yes-->Y;
    A--no-->E;

    E[Do you need strict RFC 3339 parsing?];
    E--yes-->Y;
    E--no-->H;

    H[Do you need to support Python < 3.11?]
    H--yes-->I;
    H--no-->Z;

    I[Do you need to support Python < 3.8?]
    I--yes-->W;
    I--no-->V;

    V[Use backports.datetime_fromisoformat]
    W[Use ciso8601 v2.x]
    Y[Use ciso8601]
    Z[Use datetime.fromisoformat]
```

## Do you care about the performance of timestamp parsing?

In most Python programs, performance is not a primary concern.
Even for performance-sensitive programs, timestamp parsing performance is often a negligible portion of the time spent, and not a performance bottleneck.

**Note:** Since Python 3.11+, the performance of cPython's `datetime.fromisoformat` is now very good. See [the benchmarks](https://github.com/closeio/ciso8601#benchmark).

If you really, truly want to use the fastest parser, then `ciso8601` aims to be the fastest. See [the benchmarks](https://github.com/closeio/ciso8601#benchmark) to see how it compares to other options.

## Do you need strict RFC 3339 parsing?

RFC 3339 can be (roughly) thought of as a subset of ISO 8601. If you need strict timestamp parsing that will complain if the given timestamp isn't strictly RFC 3339 compliant, then [`ciso8601` has a `parse_rfc3339` method](https://github.com/closeio/ciso8601#strict-rfc-3339-parsing).

## Do you need to support Python < 3.11?

Since Python 3.11, `datetime.fromisoformat` supports parsing nearly any ISO 8601 timestamp, and the cPython implementation is [very performant](https://github.com/closeio/ciso8601#benchmark).

If you need to support older versions of Python 3, consider [`backports.datetime_fromisoformat`](https://github.com/movermeyer/backports.datetime_fromisoformat).

## Do you need to support Python < 3.8?

`ciso8601` v3.x requires Python 3.8 or newer. If you need to support Python 2.7 or Python 3.4-3.7, you can use [`ciso8601` v2.x](https://github.com/closeio/ciso8601/tree/v2.3.1), which supports these older Python versions.
