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
import re, os

import pinyin_to_zhuyin_table as pz
import collections

class Dictionary ():
  """ A class containing some data from a dic and some methods along with them.

  Call: Dictionary(1,2,3,4,5)
  Arguments:
   1: a list of simplified forms
   2: a list of traditional forms
   3: a list of translations
   4: a list of pinyin
   5: a list of zhuyin (default = [])
  
  """
  def __init__(self, a, b, c, d, e=[]):
    self.simplified = a
    self.traditional = b
    self.translation = c
    self.pinyin = d
    self.zhuyin = e
    self.index_list = []

  def pinyin_to_zhuyin(self, pinyin):
    """Converts the given pinyin list into zhuyin. Returns a list."""
    pinyin_zhuyin_dict = pz.pinyin_to_zhuyin

    # for speed issue, transforme the list of pinyin in one long string
    to_convert = " " + " # ".join(pinyin)
    to_convert += " " # This space is useful for the regexp matching
    to_convert = to_convert.lower()
    zhuyin = re.sub("u:","ü", to_convert)    # change u: into ü
    zhuyin = re.sub(" r "," er ", zhuyin)        # change r into er
    for i in range(len(pinyin_zhuyin_dict)):
      if i < len(pinyin_zhuyin_dict)-5:
        zhuyin = re.sub(" "+pinyin_zhuyin_dict[i][0],
                        " "+pinyin_zhuyin_dict[i][1],
                        zhuyin)   # do not change the tones
      if i >= len(pinyin_zhuyin_dict)-5:
        zhuyin = re.sub(pinyin_zhuyin_dict[i][0]+" ",
                        pinyin_zhuyin_dict[i][1]+" ",
                        zhuyin) # tones
    # delete the last space used for matching convenience
    zhuyin = zhuyin[:-1]
    # Break the long string as a list and save it
    zhuyin = zhuyin.split(" # ")
    zhuyin[0] = zhuyin[0][1:] # get rid of the first space

    return zhuyin

  def unicode_pinyin(self, pin1yin1):
    """ Convert a string representing a pinyin syllable with tone. Returns a
    string.
    
    Argument:
     A string like "ni3".
    
    """
    syl = pin1yin1[:-1]
    tone = int(pin1yin1[-1])
    first_tone = "āēīōūǖ"
    second_tone = "áéíóúǘ"
    third_tone = "ǎěǐǒǔǚ"
    fourth_tone = "àèìòùǜ"
    fifth_tone = "aeiouü"
    tones = [first_tone, second_tone, third_tone, fourth_tone, fifth_tone]
    def find_vowels(string):
      """Returns a list of the vowels found, in order, as a list."""
      vowels_list = "aeiouü"
      vowels_places = [string.find(x) for x in vowels_list]
      output = ["", "", "", "", ""]
      for i in range(len(vowels_places)):
        if vowels_places[i] != -1:
          output[vowels_places[i]] = vowels_list[i]
      return output
    def is_there_iu(vowels_list):
      """Check if "iu" is in the pinyin string. Returns a boolean."""
      for i in range(len(vowels_list)):
        if vowels_list[i] != vowels_list[-1]:
          if vowels_list[i] == "i" and vowels_list[i+1] == "u":
            return True
          return False
    vowels = find_vowels(syl)
    if is_there_iu(vowels) == True:
      syl = syl.replace("u", tones[tone-1][4])
      return syl
    # To check, in order: 'a','o','e','i','u','ü' (cf. wiki)
    if "a" in vowels:
      syl = syl.replace("a", tones[tone-1][0])
      return syl
    if "o" in vowels:
      syl = syl.replace("o", tones[tone-1][3])
      return syl
    if "e" in vowels:
      syl = syl.replace("e", tones[tone-1][1])
      return syl
    if "i" in vowels:
      syl = syl.replace("i", tones[tone-1][2])
      return syl
    if "u" in vowels:
      syl = syl.replace("u", tones[tone-1][4])
      return syl
    if "ü" in vowels:
      syl = syl.replace("ü", tones[tone-1][5])
      return syl

  def write_attr(self, attr, thing):
    """Writes "thing" into self.attr, given "attr" as a string."""
    if attr == "pinyin":
      self.pinyin = thing
    elif attr == "zhuyin":
      self.zhuyin = thing
    elif attr == "simplified":
      self.simplified = thing
    elif attr == "traditional":
      self.traditional = thing
    elif attr == "translation":
      self.translation = thing
    elif attr == "index_list":
      self.index_list =  thing
    elif True:
      print(" Attribute "+attr+" is not defined for this class.")

  def search(self, given_list, text):
    """ Search for a string in a list.

    Arguments:
     given_list: a list of words
     text: a string

    Searchs for "string" in "given_list". Returns a list of indices in the
    index_list attribute of the Data class.
    
    """
    words = (text.lower()).split()
    index = []
    total = []
    for k in range(len(given_list)): # try in each line of the dic
      counter = 0
      for s in range(len(words)):
        # for each word of the request (case insensitive)
        if (given_list[k].lower()).count(words[s]) != 0:
          counter = counter +1
        if counter == len(words):
          # only accepts lines containing every words
          index.append(k)
          total.append(len(given_list[k]))
    d = dict(zip(index,total))
    dl = sorted(d.items(), key=lambda x: x[1])
    index = []
    for i in range(len(dl)): # Keep the sorted results
      index.append(dl[i][0])
    self.write_attr("index_list", index)

class ChineseTable ():
  """Contains data and name of a Chinese table input method."""
  def __init__(self, table_path):
    self.characters_list = collections.defaultdict()
    self.keys_faces = []
    self.keys_displayed_faces = []
    self.table_path = table_path

  def get_keys(character):
    code = self.characters_list[character]
    to_display = ""
    for c in code:
      where = self.keys_faces.rfind(c)
      to_display = to_display + self.keys_displayed_faces[where]
    return to_display

  def proceed(self, char):
    """ Returns the key code of the character as a code and as displayed_faces."""
    output = []
    if char not in self.characters_list:
      code = char
      displayed_code = char
    else:
      code = self.characters_list[char]
      displayed_code = ""
      for letter in code:
        letter_pos = self.keys_faces.rfind(letter)
        displayed_code += self.keys_displayed_faces[letter_pos]
    output.append(code)
    output.append(displayed_code)
    return output

class Cangjie5Table (ChineseTable):
  """Contains the full cangjie5 input method information."""
  def load(self):
    """Loads the file and saves it in the attribute (self.characters_list)."""
    with open(self.table_path, "r") as cangjie_file:
      lines = cangjie_file.readlines()
    for line in lines:
      space_pos = line.rfind(" ")
      keys = line[0:space_pos]
      char = line[space_pos+1:-1]
      self.characters_list[char] = keys

    # Set the keys and keys_faces
    self.keys_faces = "abcdefghijklmnopqrstuvwxyz"
    self.keys_displayed_faces = "日月金木水火土竹戈十大中一弓人心手口尸廿山女田難卜重"

class Array30Table (ChineseTable):
  """Contains the full Array30 input method information."""
  def load(self):
    """Loads the file and saves it in the attribute (self.characters_list)."""
    with open(self.table_path, "r") as cangjie_file:
      lines = cangjie_file.readlines()
    for line in lines:
      space_pos = line.rfind(" ")
      keys = line[0:space_pos]
      char = line[space_pos+1:-1]
      self.characters_list[char] = keys

    # Set the keys and keys_faces
    self.keys_faces = "qwertyuiopasdfghjkl;zxcvbnm,./"
    self.keys_displayed_faces = "1↑", "2↑", "3↑", "4↑", "5↑", "6↑", "7↑", "8↑", "9↑", "0-", "1-", "2-", "3-", "4-", "5-", "6-", "7-", "8-", "9-", "0-", "1↓", "2↓", "3↓", "4↓", "5↓", "6↓", "7↓", "8↓", "9↓", "0↓"

class Wubi86Table (ChineseTable):
  """Contains the full Wubi86 input table information."""
  def load(self):
    """Loads the file and saves is in the attribute (self.characters_list)"""
    with open(self.table_path, "r") as cangjie_file:
      lines = cangjie_file.readlines()
      for line in lines:
        space_pos = line.rfind(" ")
        keys = line[0:space_pos]
        char = line[space_pos+1:-1]
        self.characters_list[char] = keys

    # Set the keys and keys_faces
        self.keys_faces = "abcdefghijklmnopqrstuvwxyz"
        self.keys_displayed_faces = "abcdefghijklmnopqrstuvwxyz"
