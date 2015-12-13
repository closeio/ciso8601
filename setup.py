from setuptools import setup, Extension

setup(
    name="ciso8601",
    version="1.0.1",
    description='Fast ISO8601 date time parser for Python written in C',
    license="MIT",
    ext_modules=[Extension("ciso8601", ["module.c"])],
    test_suite='tests',
    tests_require=['pytz'],
)
