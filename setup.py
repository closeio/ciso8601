import os

from setuptools import setup, Extension
# workaround for open() with encoding='' python2/3 compatibility
from io import open

with open('README.rst', encoding='utf-8') as file:
    long_description = file.read()


# We want to force all warnings to be considered errors.
# We can't use `extra_compile_args`, since the cl.exe (Windows) and gcc compilers don't use the same flags.
# Further, there is not an easy way to tell which compiler is being used.
# Instead we rely on each compiler looking at their appropriate environment variable.

# GCC/Clang
try:
    _ = os.environ['CFLAGS']
except KeyError:
    os.environ['CFLAGS'] = ""
os.environ['CFLAGS'] += " -Werror"

# cl.exe
try:
    _ = os.environ['_CL_']
except KeyError:
    os.environ['_CL_'] = ""
os.environ['_CL_'] += " /WX"

setup(
    name="ciso8601",
    version="2.0.1",
    description='Fast ISO8601 date time parser for Python written in C',
    long_description=long_description,
    url="https://github.com/closeio/ciso8601",
    license="MIT",
    ext_modules=[Extension("ciso8601", ["module.c"])],
    packages=["ciso8601"],
    package_data={"ciso8601": ["__init__.pyi", "py.typed"]},
    test_suite='tests',
    tests_require=[
        'pytz',
        "unittest2 ; python_version < '3'"
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
