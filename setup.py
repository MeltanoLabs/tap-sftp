#!/usr/bin/env python
from setuptools import setup


with open('requirements.txt', 'r') as fh:
    requirements = fh.read().splitlines()

setup(
    name="tap-sftp",
    version="1.0.2",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_sftp"],
    install_requires=requirements,
    entry_points="""
    [console_scripts]
    tap-sftp=tap_sftp.tap_sftp:main
    """,
    packages=["tap_sftp", "tap_sftp.singer_encodings"]
)
