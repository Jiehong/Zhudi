#!/usr/bin/env python
# coding: utf-8

import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name="zhudi",
    version="1.5",
    description="Zhudi is a graphical interface to xDICT dictionaries",
    long_description=README,
    author="Jiehong Ma",
    author_email="ma.jiehong at gmail",
    url="https://github.com/Jiehong/Zhudi",
    license="GPLv3",
    packages=find_packages(),
    scripts=[
        'scripts/zhudi',
        'scripts/zhu',
        'scripts/zhudi_gui.py',
        'scripts/zhudi_cli.py',
    ],
    data_files=[('share/zhudi-data', ['zhudi-data/array30',
                                      'zhudi-data/cangjie5',
                                      'zhudi-data/wubi86'])])
