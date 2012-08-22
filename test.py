#!/usr/bin/env python
# coding=utf8
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
#   You can run all the tests by simply launching "python test.py"
#
# TODO (assertEqual(a,b), assertTrue(a), assertRaises(error_name))
import unittest

# Add here the part you want to test if it is a new one
import data

class TestDataDictionaryFunctions(unittest.TestCase):
  """ TestDataFunctions aims to test functions defined in data.py,
   and especially the ones in the Dictionary class. """

  def setUp(self):
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
    self.dictionary = data.Dictionary(simp,trad,trans,pin,zhu)

  def test_pinyin_to_zhuyin(self):
    """ Test pinyin_to_zhuyin conversion function. """
    pinyin = ["fei1",
              "fei2",
              "fei3",
              "fei4",
              "fei5",
              "fei1 chang2"]
    zhuyin_ref = ["ㄈㄟ",
                  "ㄈㄟˊ",
                  "ㄈㄟˇ",
                  "ㄈㄟˋ",
                  "ㄈㄟ˙",
                  "ㄈㄟ ㄔㄤˊ"]
    zhuyin_test = self.dictionary.pinyin_to_zhuyin(pinyin)
    self.assertEqual(zhuyin_ref, zhuyin_test)

  def test_write_attr(self):
    """
    Test write_attr function. This function saves a list in an existing
    attribute of the Dictionary class.
    
    """
    # Good case
    list_ref = [1, 2, 3, 4]
    attr = "pinyin"
    self.dictionary.write_attr(attr, list_ref)
    self.assertEqual(list_ref, self.dictionary.pinyin)
  
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

        text  = "bye"
        -> [1]
    
    """

    given_list = ["Hello", "Bye", "Hello Fred", "Python"]
    text = "Hello"
    self.dictionary.search(given_list,text)
    self.assertEqual(self.dictionary.index_list,[0, 2])

    text = "bye"
    self.dictionary.search(given_list,text)
    self.assertEqual(self.dictionary.index_list,[1])

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
        resulting_list.append(self.dictionary.unicode_pinyin(k))
      self.assertEqual(resulting_list, expected_list)

if __name__ == '__main__':
  unittest.main()
