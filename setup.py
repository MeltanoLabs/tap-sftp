#!/usr/bin/env python
from setuptools import setup


with open('requirements.txt', 'r') as fh:
    requirements = fh.read().splitlines()

setup(
    name="tap-nicesftp",
    version="2.1.2",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_nicesftp"],
    install_requires=requirements,
    entry_points="""
    [console_scripts]
    tap-nicesftp=tap_nicesftp.tap:main
    """,
    packages=["tap_nicesftp", "tap_nicesftp.singer_encodings"]
)
