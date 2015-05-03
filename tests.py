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

#
# This is the unitests part of Zhudi.
#
# You can run all the tests by simply launching "python test.py"
#
# TODO (assertEqual(a,b), assertTrue(a), assertRaises(error_name))
import unittest

# Add here the part you want to test if it is a new one
import zhudi

def setup():
    """ Initialisation needed by functions of Dictionary class. """
    with open("simplified", mode="r") as simp_file:
        simp = simp_file.readlines()
    with open("traditional", mode="r") as trad_file:
        trad = trad_file.readlines()
    with open("translation", mode="r") as trans_file:
        trans = trans_file.readlines()
    with open("pinyin", mode="r") as pin_file:
        pin = pin_file.readlines()
    with open("zhuyin", mode="r") as zhu_file:
        zhu = zhu_file.readlines()
    array30_obj = zhudi.chinese_table.Array30Table()
    array30_dic, array30_short = array30_obj.load("zhudi-data/array30")
    cangjie5_obj = zhudi.chinese_table.Cangjie5Table()
    cangjie5_dic, cangjie5_short = cangjie5_obj.load("zhudi-data/cangjie5")
    wubi86_obj = zhudi.chinese_table.Wubi86Table()
    wubi86_dic, wubi86_short = wubi86_obj.load("zhudi-data/wubi86")
    return zhudi.data.Data(simp, trad, trans,
                           wubi86_dic, wubi86_short,
                           array30_dic, array30_short,
                           cangjie5_dic, cangjie5_short,
                           pin, zhu)

global DATA_OBJ
DATA_OBJ = setup()

class TestZhudiProcessing(unittest.TestCase):
    """ Test functions in processing.py. """

    def setUp(self):
        """ Prerequisite function. """
        self.dic_tools = zhudi.processing.DictionaryTools()
        self.seg_tools = zhudi.processing.SegmentationTools()
        self.seg_tools.load(DATA_OBJ)

    def test_pinyin_to_zhuyin(self):
        """ Test pinyin_to_zhuyin conversion function. """
        pinyin = [
            "fei1",
            "fei2",
            "fei3",
            "fei4",
            "fei5",
            "fei1 chang2",
        ]
        zhuyin_ref = [
            "ㄈㄟ",
            "ㄈㄟˊ",
            "ㄈㄟˇ",
            "ㄈㄟˋ",
            "ㄈㄟ˙",
            "ㄈㄟ ㄔㄤˊ",
        ]
        zhuyin_test = self.dic_tools.pinyin_to_zhuyin(pinyin, DATA_OBJ)
        self.assertEqual(zhuyin_ref, zhuyin_test)

    def test_search(self):
        """ Test search function. This function returns the list of index
        where the text is found in the list. This function is not case
        sensitive. This function also search for words inside a string.

        This index list is sorted: first are complete matches and then partial
        matches.
        The resulting index list is saved in Dictionary.index_list

        Ex: list = ["Hello", "Bye", "Hello Fred", "Python"]
            text = "Hello"
            -> [0, 2]

            text = "bye"
            -> [1]

        """

        given_list = ["Hello", "Bye", "Hello Fred", "Python"]
        text = "Hello"
        self.dic_tools.search(given_list, text)
        self.assertEqual(self.dic_tools.index, [0, 2])

        text = "bye"
        self.dic_tools.search(given_list, text)
        self.assertEqual(self.dic_tools.index, [1])

    def test_unicode_pinyin(self):
        """
        Test unicode_pinyin function.
        This function returns a pinyin representation with unicode characters.
        This function only works for one syllable.

        Ex: pin1 -> pīn

        """
        given_list = ["pin1", "jia3", "jiu4", "hui4", "biao2", "ma5"]
        expected_list = ["pīn", "jiǎ", "jiù", "huì", "biáo", "ma"]
        resulting_list = []
        for k in given_list:
            resulting_list.append(self.dic_tools.unicode_pinyin(k))
        self.assertEqual(resulting_list, expected_list)

    def test_sentence_segmentation(self):
        """
        Test sentence_segmentation function (in ChineseProcessing class).
        This function returns a list of words given a sentence.
        Its results depends on the dictionary.

        Ex: 我以為你不想再見我了
        --> ['我', '以為', '你', '不想', '再見', '我', '了']

        """
        given_sentence = "我以為你不想再見我了"
        expected_result = ['我', '以為', '你', '不想', '再見', '我', '了']
        actual_result = self.seg_tools.sentence_segmentation(given_sentence)
        self.assertEqual(actual_result, expected_result)

    def test_search_unique(self):
        """ Test search_unique function.
        This function returns and index (exact matches) or None if nothing found.
        (It only works for Chinese!)
        """

        class Fdo(object):
            """ Dummy local class. """

            def __init__(self):
                self.traditional = ["我", "你", "我你", "再見"]
                self.simplified = self.traditional

        fake_data_obj = Fdo()
        given_good_word = "我"
        expected_good_result = 0
        actual_good_result = self.seg_tools.search_unique(given_good_word, fake_data_obj)
        self.assertEqual(actual_good_result, expected_good_result)

        given_bad_word = "以為"
        expected_bad_result = None
        actual_bad_result = self.seg_tools.search_unique(given_bad_word, fake_data_obj)
        self.assertEqual(actual_bad_result, expected_bad_result)

    def test_is_not_chinese(self):
        """ Test is_not_chinese, which purpose is to test
        if the given string is Chinese or not.
        returns True (if not chinese) or False (if chinese)
        """

        given_string = "以為"
        expected_result = False
        actual_result = self.seg_tools.is_not_chinese(given_string)
        self.assertEqual(actual_result, expected_result)

        given_string = "hello"
        expected_result = True
        actual_result = self.seg_tools.is_not_chinese(given_string)
        self.assertEqual(actual_result, expected_result)

# class TestZhudiChineseTable(unittest.TestCase):
#     def test_proceed(self):
#         pass

#     def test_load(self):
#         pass

if __name__ == '__main__':
    unittest.main()
