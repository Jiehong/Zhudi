#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages


setup(
    name="zhudi",
    version="1.4",
    description="Zhudi is a graphical interface to xDICT dictionaries",
    long_description="Have a look at README.",
    author="Jiehong Ma",
    author_email="ma.jiehong at gmail",
    url="https://github.com/Jiehong/Zhudi",
    license="GPLv3",
    packages=find_packages(),
    py_modules=[
        "gui",
        "cli",
        "zhudi",
        "zhudi_data",
        "zhudi_processing",
        "zhudi_chinese_table",
    ],
    scripts=[
        'zhudi',
        'zhu',
    ],
    data_files=[('share/zhudi-data', ['zhudi-data/array30',
                                      'zhudi-data/cangjie5',
                                      'zhudi-data/wubi86'])])
