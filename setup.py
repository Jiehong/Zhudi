#!/usr/bin/env python

from distutils.core import setup

setup(name="Zhudi",
      version="1.1",
      description="Zhudi is a graphical interface to xDICT dictionaries",
      long_description="Zhudi is a graphical interface to CEDICT, CFDICT,"+
      "HanDeDict and ChE-Dicc. Therefore, it allows you to have a Chinese to"+
      "English, French, German and Spanish dictionary.",
      author="Jiehong Ma",
      author_email="ma.jiehong at gmail",
      url="https://github.com/Jiehong/Zhudi",
      license="GPLv3",
      py_modules=["main", "data", "gui", "pinyin_to_zhuyin_table"])
