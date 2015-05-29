#!/usr/bin/env python
# coding: utf-8
''' Zhudi provides a Chinese - language dictionnary based on the
    C[E|F]DICT project Copyright - 2011 - Ma Jiehong

    Zhudi is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Zhudi is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
    License for more details.

    You should have received a copy of the GNU General Public License
    If not, see <http://www.gnu.org/licenses/>.

'''

import os
import argparse

from zhudi import data, processing, chinese_table


class WrongInputException(Exception):
    """
    Dummy class used to silent an exception.

    """
    pass

# Function to locate the data folder
#_ROOT = os.path.abspath(os.path.dirname(__file__))
_ROOT = "/usr/share/"


def get_data_path(path):
    """
    Compute the correct path to find data.

    """
    return os.path.join(_ROOT, 'zhudi-data', path)

def prepare_data(options, data_proxy):
    """
    Split the dictionary input, and compute the zhuyin equivalent as well.
    Values are stored in the data actor (by proxy).

    """
    filename = options.filename
    pinyin_file_name = options.pinyin_file_name
    zhuyin_file_name = options.zhuyin_file_name
    simplified_file_name = options.simplified_file_name
    translation_file_name = options.translation_file_name
    traditional_file_name = options.traditional_file_name

    preproc_o = processing.PreProcessing()
    files = [pinyin_file_name,
             zhuyin_file_name,
             traditional_file_name,
             simplified_file_name,
             translation_file_name]
    default_files = [os.environ["HOME"] + "/.zhudi/pinyin",
                     os.environ["HOME"] + "/.zhudi/zhuyin",
                     os.environ["HOME"] + "/.zhudi/traditional",
                     os.environ["HOME"] + "/.zhudi/simplified",
                     os.environ["HOME"] + "/.zhudi/translation"]
    # Splitting the given input
    passed = False
    if (filename is not None) and all(x is None for x in files):
        print("Splitting dictionary in progress…")
        files = preproc_o.split(filename)
        simplified_list = files[0]
        traditional_list = files[1]
        translation_list = files[2]
        pinyin_list = files[3]

        data_proxy.simplified = simplified_list
        data_proxy.traditional = traditional_list
        data_proxy.translation = translation_list
        data_proxy.pinyin = pinyin_list

        print("\nPinyin to Zhuyin conversion in progress…")
        dic_tools_obj = processing.DictionaryTools()
        zhuyin = dic_tools_obj.pinyin_to_zhuyin(pinyin_list, data_proxy)
        data_proxy.zhuyin = zhuyin

        # Saves the Zhuyin list into a file
        with open("zhuyin", mode="w") as zhuyin_file:
            for line in zhuyin:
                zhuyin_file.write(line+"\n")
        print("done.")
        quit()

    # First case scenario: no arguments given but defaults files are found
    elif all(x is None for x in files):
        temp_value = 0
        for a_file in default_files:
            if os.path.isfile(a_file) is True:
                temp_value += 1
        if temp_value == len(default_files):
            (pinyin, zhuyin, traditional,
             simplified, translation) = preproc_o.read_files(
                 default_files[0],
                 default_files[1],
                 default_files[2],
                 default_files[3],
                 default_files[4])
            passed = True
        else:
            print("### No input files have been given to me. Please, consider" +
                  " giving me some. ###")
            quit()
    # Second scenario: all files passed as arguments, load them
    elif all(x is not None for x in files):
        (pinyin, zhuyin, traditional,
         simplified, translation) = preproc_o.read_files(
             files[0],
             files[1],
             files[2],
             files[3],
             files[4])
        passed = True
    # Third scenario: some input files are missing
    elif None in files:
        print("You must pass all generated files if launched manually")
        print("Try with:\n")
        print("\t-p pinyin -tr translation -sd simplified -z zhuyin -td traditional")
        quit()
    # Last scenario: No input -> help
    elif (filename is None) and all(x is None for x in files) and not passed:
        raise WrongInputException

    # Load the cangjie infos
    cangjie5_obj = chinese_table.Cangjie5Table()
    cangjie_dic, cangjie_short_dic = cangjie5_obj.load(get_data_path('cangjie5'))
    # Load array30 infos
    array30_obj = chinese_table.Array30Table()
    array_dic, array_short_dic = array30_obj.load(get_data_path('array30'))
    # Load wubi86 infos
    wubi86_obj = chinese_table.Wubi86Table()
    wubi_dic, wubi_short_dic = wubi86_obj.load(get_data_path('wubi86'))

    # Data object
    data_proxy.simplified = simplified
    data_proxy.traditional = traditional
    data_proxy.translation = translation
    data_proxy.wubi86 =  wubi_dic
    data_proxy.wubi86_short = wubi_short_dic
    data_proxy.array30 = array_dic
    data_proxy.array30_short = array_short_dic
    data_proxy.cangjie5 = cangjie_dic
    data_proxy.cangjie5_short = cangjie_short_dic
    data_proxy.pinyin = pinyin
    data_proxy.zhuyin = zhuyin
    data_proxy.load_config()

def get_argument_parser():
    """
    Handle parsing the input arguments.

    """

    parser = argparse.ArgumentParser(description='Provide a graphical interface'
                                     ' for *.u8 dictionaries (CEDICT, CFDICT…)')
    parser.add_argument("-s", "--split", dest="filename", help="The *.u8"
                        " dictionary file to be split. This operation will be"
                        " done in the current directory.")
    parser.add_argument("-p", "--pinyin-file", dest="pinyin_file_name",
                        help="The file that contains the pinyin. This file comes"
                        "from the split of the *.u8 dictionary file.")
    parser.add_argument("-z", "--zhuyin-file", dest="zhuyin_file_name",
                        help="The file that contains the zhuyin. This file comes"
                        "from the split of the *.u8 dictionary file.")
    parser.add_argument("-tr", "--translation-file", dest="translation_file_name",
                        help="The file that contains the translation. This file"
                        " comes from the split of the *.u8 dictionary file.")
    parser.add_argument("-td", "--traditional-file", dest="traditional_file_name",
                        help="The file that contains the traditional form of the"
                        " Chinese. This file comes from the split of the *.u8"
                        " dictionary file.")
    parser.add_argument("-sd", "--simplified-file", dest="simplified_file_name",
                        help="The file that contains the simplified form of the"
                        " Chinese. This file comes from the split of the *.u8"
                        " dictionary file.")
    return parser
