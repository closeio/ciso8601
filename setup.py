import os

from setuptools import setup, Extension

# workaround for open() with encoding='' python2/3 compatibility
from io import open

with open("README.rst", encoding="utf-8") as file:
    long_description = file.read()

# We want to force all warnings to be considered errors. That way we get to catch potential issues during
# development and at PR review time.
# But since ciso8601 is a source distribution, exotic compiler configurations can cause spurious warnings that
# would fail the installation. So we only want to treat warnings as errors during development.
if os.environ.get("STRICT_WARNINGS", "0") == "1":
    # We can't use `extra_compile_args`, since the cl.exe (Windows) and gcc compilers don't use the same flags.
    # Further, there is not an easy way to tell which compiler is being used.
    # Instead we rely on each compiler looking at their appropriate environment variable.

    # GCC/Clang
    try:
        _ = os.environ["CFLAGS"]
    except KeyError:
        os.environ["CFLAGS"] = ""
    os.environ["CFLAGS"] += " -Werror"

    # cl.exe
    try:
        _ = os.environ["_CL_"]
    except KeyError:
        os.environ["_CL_"] = ""
    os.environ["_CL_"] += " /WX"

VERSION = "2.3.2"
CISO8601_CACHING_ENABLED = int(os.environ.get('CISO8601_CACHING_ENABLED', '1') == '1')

setup(
    name="ciso8601",
    version=VERSION,
    description="Fast ISO8601 date time parser for Python written in C",
    long_description=long_description,
    url="https://github.com/closeio/ciso8601",
    license="MIT",
    ext_modules=[
        Extension(
            "ciso8601",
            sources=["module.c", "timezone.c", "isocalendar.c"],
            define_macros=[
                ("CISO8601_VERSION", VERSION),
                ("CISO8601_CACHING_ENABLED", CISO8601_CACHING_ENABLED),
            ],
        )
    ],
    packages=["ciso8601"],
    package_data={"ciso8601": ["__init__.pyi", "py.typed"]},
    test_suite="tests",
    tests_require=[
        "pytz",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
