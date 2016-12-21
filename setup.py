from setuptools import setup, Extension

setup(
    name="ciso8601",
    version="1.0.3",
    description='Fast ISO8601 date time parser for Python written in C',
    license="MIT",
    ext_modules=[Extension("ciso8601", ["module.c"])],
    test_suite='tests',
    tests_require=['pytz'],
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
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
