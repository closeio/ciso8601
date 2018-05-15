from setuptools import setup, Extension
# workaround for open() with encoding='' python2/3 compability
from io import open

with open('README.rst', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name="ciso8601",
    version="2.0.0",
    description='Fast ISO8601 date time parser for Python written in C',
    long_description=long_description,
    license="MIT",
    ext_modules=[Extension("ciso8601", ["module.c"])],
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
