# What is Zhudi?
Zhudi is a graphical interface to CEDICT, CFDICT, HanDeDict, ChE-Dicc). Therefore, it allows you to have a Chinese to English, French, German and Spanish dictionary.

Zhudi is designed to help users by providing them good choices. Consequently, a Bopomofo engine is included to provide pronunciation along with pinyin. Traditional and simplified characters are fully supported too.

# What platforms are supported?
Since this project is written in Python 3, it should be able to run on any given platform. However, I only have tested it under GNU/Linux.

Currently, Zhudi can easily be installed on Archlinux from AUR.

# What are the dependencies of Zhudi?
In order to run Zhudi, you need the following packages:
* python 3+
* python-gobject
* pygobject-devel
* gobject-introspection

# Versions
Version 0.9 is made to work with python2 and is now obsolete. You should use version 1.0 and later instead.

# Launching
Zhudi can be launched from the command line by providing it proper files.

## First launch
When you first launch Zhudi, you need to provide a dictionary file. You are free to use the one you like among:
* [CEDICT](http://www.mdbg.net/chindict/chindict.php?page=cedict) for English-Chinsese ;
* [CFDICT](http://www.chine-informations.com/chinois/open/CFDICT/) for French-Chinese ;
* [HanDeDict](http://www.handedict.de/chinesisch_deutsch.php) For German-Chinese ;
* [ChE-DICC](http://cc-chedicc.wikispaces.com/) for Spanish-Chinese.

You have to download the *.u8 version of the dictionary for using with Zhudi. Once you have downloaded it, simply run Zhudi to prepare the dictionary for future uses. Here is an example with the CEDICT dictionary (cedict.u8):

    python zhudi.py -s cedict.u8

When Zhudi is finished, it would have created 5 files: pinyin, zhuyin, simplified, traditional and translation.

## Normal usage
When the previous 5 files are created, you can simply launch Zhudi:

    python zhudi.py -p pinyin -z zhuyin -tr translation -td traditional -sd simplified
    
However, in order not to type that command each time, you can simply launch the launch.sh shell script.
