#!/usr/bin/env python
from distutils.core import setup
# coding: utf-8

setup(
    name="zhudi",
    version="1.3",
    description="Zhudi is a graphical interface to xDICT dictionaries",
    long_description="Have a look at README.",
    author="Jiehong Ma",
    author_email="ma.jiehong at gmail",
    url="https://github.com/Jiehong/Zhudi",
    license="GPLv3",
    py_modules=["gui", "zhudi_data", "zhudi_processing", "zhudi_chinese_table"],
    scripts=['zhudi'],
    data_files=[('share/zhudi-data', ['zhudi-data/array30',
                                      'zhudi-data/cangjie5',
                                      'zhudi-data/wubi86'])])
