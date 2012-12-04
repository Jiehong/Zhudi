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

import collections

class PreProcessing ():
  """This class is in charge of the pre-processing needed to lauch Zhudi.
  It loads config files, split dictionaries, etc.
  
  """
  def __init__(self):
    pass

  def split(self, dictname):
    """Loads the *.u8 file and split it. Return a tuple of 4 lists:
    (simplified_list,
    traditional_list,
    translation_list,
    pinyin_list)
    """
    dictionary = dictname
    # Open the dictionary in text mode, read only
    with open(dictionary, mode="r") as dic:
      liste = dic.readlines() # Use the text file as lines
    space_ind = []
    pinyin_delimiters = []
    translation_delimiters = []
    simplified_list = []
    traditional_list = []
    pinyin_list = []
    translation_list = []

    simplified_file = open("simplified", mode="w")
    traditional_file = open("traditional", mode="w")
    translation_file = open("translation", mode="w")
    pinyin_file = open("pinyin", mode="w")
    for i in liste: # for each line
      space_ind = []
      pinyin_delimiters = []
      translation_delimiters = []
      translation = []

      if i[0] != "#":
        for k in range(len(i)):
          if i[k] == " ": # look for spaces
            space_ind.append(k)
          if i[k] == "[": # look for pinyin delimiters
            pinyin_delimiters.append(k)
          if i[k] == "]":
            pinyin_delimiters.append(k)
          if i[k] == "/": # look for translation delimiters
            translation_delimiters.append(k)
        traditional = i[0:space_ind[0]]
        simplified = i[space_ind[0]+1:space_ind[1]]
        pinyin = i[pinyin_delimiters[0]+1:pinyin_delimiters[1]]
        for n in range(len(translation_delimiters)-1):
          translation.append(i[translation_delimiters[n]+1
                               :translation_delimiters[n+1]])
        # Get rid of sticking pinyin like di4shang4 instead of di4 shang4
        clean_pinyin = ""
        for n in range(len(pinyin)):
          clean_pinyin += pinyin[n]
          if pinyin[n].isdigit() and (n < len(pinyin)-1):
            if pinyin[n+1] != " ":
              clean_pinyin += " "
        translation_clean = ""
        for i in range(len(translation)):
          if i != 0:
            translation_clean += "/"
          translation_clean += translation[i]

        pinyin_list.append(clean_pinyin)
        traditional_list.append(traditional)
        simplified_list.append(simplified)
        translation_list.append(translation_clean)

        simplified_file.write(simplified+"\n")
        traditional_file.write(traditional+"\n")
        translation_file.write(translation_clean+"\n")
        pinyin_file.write(clean_pinyin+"\n")
    simplified_file.close()
    traditional_file.close()
    translation_file.close()
    pinyin_file.close()
    return (simplified_list,
            traditional_list,
            translation_list,
            pinyin_list)
    # End of split()

  def read_files(self,
                 pinyin_file_name,
                 zhuyin_file_name,
                 traditional_file_name,
                 simplified_file_name,
                 translation_file_name):
    """Reads some files needed to build the Dictionary class.
    Returns 5 lists:
    (pinyin, zhuyin, traditional, simplified, translation)
    """
    try:
      pinyin_file = open(pinyin_file_name,"r")
      pinyin = pinyin_file.readlines()
      pinyin_file.closed
      zhuyin_file = open(zhuyin_file_name,"r")
      zhuyin = zhuyin_file.readlines()
      zhuyin_file.closed
      traditional_file = open(traditional_file_name,"r")
      traditional = traditional_file.readlines()
      traditional_file.closed
      simplified_file = open(simplified_file_name,"r")
      simplified = simplified_file.readlines()
      simplified_file.closed
      translation_file = open(translation_file_name,"r")
      translation = translation_file.readlines()
      translation_file.closed
      return pinyin, zhuyin, traditional, simplified, translation
    except(IOError) as errno:
      print("### The dictionary files couldn't be read. Make sure you have"+
            " split the dictonary file first. ###")
      quit()
    # End of read_files()
      
  def get_config(self):
    """ Reads the config file, if it exists, and returns a list of variables
    related to that file (of the form [var, value]).
    
    """
    try:
      open(os.environ["HOME"]+"/.zhudi/config", "r")
    except(IOError) as errno:
      # If no config file found
      return []
    saved_values = []
    with open(os.environ["HOME"]+"/.zhudi/config", "r") as config_file:
      lines = config_file.readlines()
      for n_line in range(len(lines)):
        if (lines[n_line][0] != "#") or (lines[n_line][0] != ""):
          if lines[n_line][:-1].lower() == "romanisation:":
            saved_values.append(["romanisation", lines[n_line+1][:-1].lower()])
          if lines[n_line][:-1].lower() == "hanzi form:":
            saved_values.append(["hanzi", lines[n_line+1][:-1].lower()])
    config_file.close()
    return saved_values

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
    pinyin_zhuyin_dict = pinyin_to_zhuyin

    # for speed issue, transforme the list of pinyin in one long string
    to_convert = " " + " # ".join(pinyin)
    to_convert += " " # This space is useful for the regexp matching
    to_convert = to_convert.lower()
    zhuyin = re.sub("u:", "ü", to_convert)    # change u: into ü
    zhuyin = re.sub(" r ", " er ", zhuyin)        # change r into er
    for i in range(len(pinyin_zhuyin_dict)):
      if i < len(pinyin_zhuyin_dict)-5:
        zhuyin = re.sub(" "+pinyin_zhuyin_dict[i][0],
                        " "+pinyin_zhuyin_dict[i][1],
                        zhuyin)   # do not change the tones
      elif i >= len(pinyin_zhuyin_dict)-5:
        zhuyin = re.sub(pinyin_zhuyin_dict[i][0]+" ",
                        pinyin_zhuyin_dict[i][1]+" ",
                        zhuyin) # tones
    # delete the last space used for matching convenience
    zhuyin = zhuyin[:-1]
    # Break the long string as a list
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
    to_test = "aoeiuü"
    for case in to_test:
      if case in vowels:
        syl = syl.replace(case, tones[tone-1][fifth_tone.find(case)])
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
    else:
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
    d = dict(zip(index, total))
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
    """ Returns the key code of the character as a code and as displayed_faces.

    """
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
    self.keys_displayed_faces = ["1↑", "2↑", "3↑", "4↑", "5↑", "6↑", "7↑", "8↑",
                                 "9↑", "0-", "1-", "2-", "3-", "4-", "5-", "6-",
                                 "7-", "8-", "9-", "0-", "1↓", "2↓", "3↓", "4↓",
                                 "5↓", "6↓", "7↓", "8↓", "9↓", "0↓"]

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

class ChineseProcessing ():
  """ This class is intended to contains any functions dealing with Chinese.
  In other words, any functions treating a sentence, a word, etc.

  """
  def __init__(self, dictionary):
    """ The Dictionary class is necessary for our functions to work. """
    self.dict = dictionary
    self.trad_set = []
    self.simp_set = []

  def load(self):
    """ Load and prepare needed data. """
    for style in [self.dict.traditional, self.dict.simplified]:
      temp = [[], [], [], [], [], [], [], [], [], [],
              [], [], [], [], [], [], [], [], [], []] # 20
      out = []
      for item in style:
        item = item[:-1] # get rid of the \n
        if len(item) <= 20:
          temp[len(item)-1].append(item)
      for nested_list in temp:
        out.append(set(nested_list)) # transform in set for performance issue
        if style == self.dict.traditional:
          self.trad_set = out
        else:
          self.simp_set = out
  # end of load()

  def sentence_segmentation(self, string):
    """ Parse the string input for Chinese words based on words in our
    dictionary. Retuns a list of words.

    """
    chars = "abcdefghijklmnopqerstuvwxyz1234567890"
    def isNotChinese(string):
      cnt = 0
      for char in string:
        if char in chars or char in chars.upper():
          cnt += 1
      if cnt == len(string):
        return True
      else:
        return False
    
    def longest_word(string):
      traditional = self.trad_set
      simplified = self.simp_set
      maxi = 20
      if len(string) < maxi:
        upper = len(string)
      else:
        upper = maxi
      for i in range(upper, 1, -1): # from max-1 to 1
        current_string = string[0:i]
        if isNotChinese(current_string):
          return current_string
        if current_string in traditional[i-1]:
          return current_string
        elif current_string in simplified[i-1]:
          return current_string
    # end of longest_word
    output = []
    while len(string) >= 1:
      lw = longest_word(string)
      if lw == None:
        lw = string[0]
        string = string[1:] # the character is alone
      else:
        string = string[len(lw):]
      output.append(lw)
    return output
# end of ChineseProcessing

pinyin_to_zhuyin = [('zhuang', 'ㄓㄨㄤ'),
                    ('shuang', 'ㄕㄨㄤ'),
                    ('chuang', 'ㄔㄨㄤ'),
                    ('zhuan', 'ㄓㄨㄢ'),
                    ('zhuai', 'ㄓㄨㄞ'),
                    ('zhong', 'ㄓㄨㄥ'),
                    ('zheng', 'ㄓㄥ'),
                    ('zhang', 'ㄓㄤ'),
                    ('xiong', 'ㄒㄩㄥ'),
                    ('xiang', 'ㄒㄧㄤ'),
                    ('shuan', 'ㄕㄨㄢ'),
                    ('shuai', 'ㄕㄨㄞ'),
                    ('sheng', 'ㄕㄥ'),
                    ('shang', 'ㄕㄤ'),
                    ('qiong', 'ㄑㄩㄥ'),
                    ('qiang', 'ㄑㄧㄤ'),
                    ('niang', 'ㄋㄧㄤ'),
                    ('liang', 'ㄌㄧㄤ'),
                    ('kuang', 'ㄎㄨㄤ'),
                    ('jiong', 'ㄐㄩㄥ'),
                    ('jiang', 'ㄐㄧㄤ'),
                    ('huang', 'ㄏㄨㄤ'),
                    ('guang', 'ㄍㄨㄤ'),
                    ('chuan', 'ㄔㄨㄢ'),
                    ('chuai', 'ㄔㄨㄞ'),
                    ('chong', 'ㄔㄨㄥ'),
                    ('cheng', 'ㄔㄥ'),
                    ('chang', 'ㄔㄤ'),
                    ('zuan', 'ㄗㄨㄢ'),
                    ('zong', 'ㄗㄨㄥ'),
                    ('zhuo', 'ㄓㄨㄛ'),
                    ('zhun', 'ㄓㄨㄣ'),
                    ('zhui', 'ㄓㄨㄟ'),
                    ('zhua', 'ㄓㄨㄚ'),
                    ('zhou', 'ㄓㄡ'),
                    ('zhen', 'ㄓㄣ'),
                    ('zhei', 'ㄓㄟ'),
                    ('zhao', 'ㄓㄠ'),
                    ('zhan', 'ㄓㄢ'),
                    ('zhai', 'ㄓㄞ'),
                    ('zeng', 'ㄗㄥ'),
                    ('zang', 'ㄗㄤ'),
                    ('yuan', 'ㄩㄢ'),
                    ('yong', 'ㄩㄥ'),
                    ('ying', 'ㄧㄥ'),
                    ('yang', 'ㄧㄤ'),
                    ('xuan', 'ㄒㄩㄢ'),
                    ('xing', 'ㄒㄧㄥ'),
                    ('xien', 'ㄒㄧㄢ'),
                    ('xiao', 'ㄒㄧㄠ'),
                    ('xian', 'ㄒㄧㄢ'),
                    ('wong', 'ㄨㄥ'),
                    ('weng', 'ㄨㄥ'),
                    ('wang', 'ㄨㄤ'),
                    ('tuan', 'ㄊㄨㄢ'),
                    ('tong', 'ㄊㄨㄥ'),
                    ('ting', 'ㄊㄧㄥ'),
                    ('tien', 'ㄊㄧㄢ'),
                    ('tiao', 'ㄊㄧㄠ'),
                    ('tian', 'ㄊㄧㄢ'),
                    ('teng', 'ㄊㄥ'),
                    ('tang', 'ㄊㄤ'),
                    ('suan', 'ㄙㄨㄢ'),
                    ('song', 'ㄙㄨㄥ'),
                    ('shuo', 'ㄕㄨㄛ'),
                    ('shun', 'ㄕㄨㄣ'),
                    ('shui', 'ㄕㄨㄟ'),
                    ('shua', 'ㄕㄨㄚ'),
                    ('shou', 'ㄕㄡ'),
                    ('shen', 'ㄕㄣ'),
                    ('shei', 'ㄕㄟ'),
                    ('shao', 'ㄕㄠ'),
                    ('shan', 'ㄕㄢ'),
                    ('shai', 'ㄕㄞ'),
                    ('seng', 'ㄙㄥ'),
                    ('sang', 'ㄙㄤ'),
                    ('ruan', 'ㄖㄨㄢ'),
                    ('rong', 'ㄖㄨㄥ'),
                    ('reng', 'ㄖㄥ'),
                    ('rang', 'ㄖㄤ'),
                    ('quan', 'ㄑㄩㄢ'),
                    ('qing', 'ㄑㄧㄥ'),
                    ('qien', 'ㄑㄧㄢ'),
                    ('qiao', 'ㄑㄧㄠ'),
                    ('qian', 'ㄑㄧㄢ'),
                    ('ping', 'ㄆㄧㄥ'),
                    ('pien', 'ㄆㄧㄢ'),
                    ('piao', 'ㄆㄧㄠ'),
                    ('pian', 'ㄆㄧㄢ'),
                    ('peng', 'ㄆㄥ'),
                    ('pang', 'ㄆㄤ'),
                    ('nuan', 'ㄋㄨㄢ'),
                    ('nong', 'ㄋㄨㄥ'),
                    ('ning', 'ㄋㄧㄥ'),
                    ('nien', 'ㄋㄧㄢ'),
                    ('niao', 'ㄋㄧㄠ'),
                    ('nian', 'ㄋㄧㄢ'),
                    ('neng', 'ㄋㄥ'),
                    ('nang', 'ㄋㄤ'),
                    ('ming', 'ㄇㄧㄥ'),
                    ('mien', 'ㄇㄧㄢ'),
                    ('miao', 'ㄇㄧㄠ'),
                    ('mian', 'ㄇㄧㄢ'),
                    ('meng', 'ㄇㄥ'),
                    ('mang', 'ㄇㄤ'),
                    ('luen', 'ㄌㄩㄢ'),
                    ('luan', 'ㄌㄨㄢ'),
                    ('long', 'ㄌㄨㄥ'),
                    ('ling', 'ㄌㄧㄥ'),
                    ('lien', 'ㄌㄧㄢ'),
                    ('liao', 'ㄌㄧㄠ'),
                    ('lian', 'ㄌㄧㄢ'),
                    ('leng', 'ㄌㄥ'),
                    ('lang', 'ㄌㄤ'),
                    ('kuan', 'ㄎㄨㄢ'),
                    ('kuai', 'ㄎㄨㄞ'),
                    ('kong', 'ㄎㄨㄥ'),
                    ('keng', 'ㄎㄥ'),
                    ('kang', 'ㄎㄤ'),
                    ('juan', 'ㄐㄩㄢ'),
                    ('jing', 'ㄐㄧㄥ'),
                    ('jien', 'ㄐㄧㄢ'),
                    ('jiao', 'ㄐㄧㄠ'),
                    ('jian', 'ㄐㄧㄢ'),
                    ('huan', 'ㄏㄨㄢ'),
                    ('huai', 'ㄏㄨㄞ'),
                    ('hong', 'ㄏㄨㄥ'),
                    ('heng', 'ㄏㄥ'),
                    ('hang', 'ㄏㄤ'),
                    ('guan', 'ㄍㄨㄢ'),
                    ('guai', 'ㄍㄨㄞ'),
                    ('gong', 'ㄍㄨㄥ'),
                    ('geng', 'ㄍㄥ'),
                    ('gang', 'ㄍㄤ'),
                    ('fong', 'ㄈㄨㄥ'),
                    ('fiao', 'ㄈㄧㄠ'),
                    ('feng', 'ㄈㄥ'),
                    ('fang', 'ㄈㄤ'),
                    ('duan', 'ㄉㄨㄢ'),
                    ('dong', 'ㄉㄨㄥ'),
                    ('ding', 'ㄉㄧㄥ'),
                    ('dien', 'ㄉㄧㄢ'),
                    ('diao', 'ㄉㄧㄠ'),
                    ('dian', 'ㄉㄧㄢ'),
                    ('deng', 'ㄉㄥ'),
                    ('dang', 'ㄉㄤ'),
                    ('cuan', 'ㄘㄨㄢ'),
                    ('cong', 'ㄘㄨㄥ'),
                    ('chuo', 'ㄔㄨㄛ'),
                    ('chun', 'ㄔㄨㄣ'),
                    ('chui', 'ㄔㄨㄟ'),
                    ('chua', 'ㄔㄨㄚ'),
                    ('chou', 'ㄔㄡ'),
                    ('chen', 'ㄔㄣ'),
                    ('chao', 'ㄔㄠ'),
                    ('chan', 'ㄔㄢ'),
                    ('chai', 'ㄔㄞ'),
                    ('ceng', 'ㄘㄥ'),
                    ('cang', 'ㄘㄤ'),
                    ('bing', 'ㄅㄧㄥ'),
                    ('bien', 'ㄅㄧㄢ'),
                    ('biao', 'ㄅㄧㄠ'),
                    ('bian', 'ㄅㄧㄢ'),
                    ('beng', 'ㄅㄥ'),
                    ('bang', 'ㄅㄤ'),
                    ('zuo', 'ㄗㄨㄛ'),
                    ('zun', 'ㄗㄨㄣ'),
                    ('zui', 'ㄗㄨㄟ'),
                    ('zou', 'ㄗㄡ'),
                    ('zhu', 'ㄓㄨ'),
                    ('zhi', 'ㄓ'),
                    ('zhe', 'ㄓㄜ'),
                    ('zha', 'ㄓㄚ'),
                    ('zen', 'ㄗㄣ'),
                    ('zei', 'ㄗㄟ'),
                    ('zao', 'ㄗㄠ'),
                    ('zan', 'ㄗㄢ'),
                    ('zai', 'ㄗㄞ'),
                    ('yun', 'ㄩㄣ'),
                    ('yue', 'ㄩㄝ'),
                    ('you', 'ㄧㄡ'),
                    ('yin', 'ㄧㄣ'),
                    ('yao', 'ㄧㄠ'),
                    ('yan', 'ㄧㄢ'),
                    ('yai', 'ㄧㄞ'),
                    ('xun', 'ㄒㄩㄣ'),
                    ('xue', 'ㄒㄩㄝ'),
                    ('xiu', 'ㄒㄧㄡ'),
                    ('xin', 'ㄒㄧㄣ'),
                    ('xie', 'ㄒㄧㄝ'),
                    ('xia', 'ㄒㄧㄚ'),
                    ('wen', 'ㄨㄣ'),
                    ('wei', 'ㄨㄟ'),
                    ('wan', 'ㄨㄢ'),
                    ('wai', 'ㄨㄞ'),
                    ('tuo', 'ㄊㄨㄛ'),
                    ('tun', 'ㄊㄨㄣ'),
                    ('tui', 'ㄊㄨㄟ'),
                    ('tou', 'ㄊㄡ'),
                    ('tie', 'ㄊㄧㄝ'),
                    ('tao', 'ㄊㄠ'),
                    ('tan', 'ㄊㄢ'),
                    ('tai', 'ㄊㄞ'),
                    ('suo', 'ㄙㄨㄛ'),
                    ('sun', 'ㄙㄨㄣ'),
                    ('sui', 'ㄙㄨㄟ'),
                    ('sou', 'ㄙㄡ'),
                    ('shu', 'ㄕㄨ'),
                    ('shi', 'ㄕ'),
                    ('she', 'ㄕㄜ'),
                    ('sha', 'ㄕㄚ'),
                    ('sen', 'ㄙㄣ'),
                    ('sei', 'ㄙㄟ'),
                    ('sao', 'ㄙㄠ'),
                    ('san', 'ㄙㄢ'),
                    ('sai', 'ㄙㄞ'),
                    ('ruo', 'ㄖㄨㄛ'),
                    ('run', 'ㄖㄨㄣ'),
                    ('rui', 'ㄖㄨㄟ'),
                    ('rou', 'ㄖㄡ'),
                    ('ren', 'ㄖㄣ'),
                    ('rao', 'ㄖㄠ'),
                    ('ran', 'ㄖㄢ'),
                    ('qun', 'ㄑㄩㄣ'),
                    ('que', 'ㄑㄩㄝ'),
                    ('qiu', 'ㄑㄧㄡ'),
                    ('qin', 'ㄑㄧㄣ'),
                    ('qie', 'ㄑㄧㄝ'),
                    ('qia', 'ㄑㄧㄚ'),
                    ('pou', 'ㄆㄡ'),
                    ('pin', 'ㄆㄧㄣ'),
                    ('pie', 'ㄆㄧㄝ'),
                    ('pen', 'ㄆㄣ'),
                    ('pei', 'ㄆㄟ'),
                    ('pao', 'ㄆㄠ'),
                    ('pan', 'ㄆㄢ'),
                    ('pai', 'ㄆㄞ'),
                    ('nuo', 'ㄋㄨㄛ'),
                    ('nüe', 'ㄋㄩㄝ'),
                    ('nou', 'ㄋㄡ'),
                    ('niu', 'ㄋㄧㄡ'),
                    ('nin', 'ㄋㄧㄣ'),
                    ('nie', 'ㄋㄧㄝ'),
                    ('nen', 'ㄋㄣ'),
                    ('nei', 'ㄋㄟ'),
                    ('nao', 'ㄋㄠ'),
                    ('nan', 'ㄋㄢ'),
                    ('nai', 'ㄋㄞ'),
                    ('mou', 'ㄇㄡ'),
                    ('miu', 'ㄇㄧㄡ'),
                    ('min', 'ㄇㄧㄣ'),
                    ('mie', 'ㄇㄧㄝ'),
                    ('men', 'ㄇㄣ'),
                    ('mei', 'ㄇㄟ'),
                    ('mao', 'ㄇㄠ'),
                    ('man', 'ㄇㄢ'),
                    ('mai', 'ㄇㄞ'),
                    ('luo', 'ㄌㄨㄛ'),
                    ('lun', 'ㄌㄨㄣ'),
                    ('lüe', 'ㄌㄩㄝ'),
                    ('lou', 'ㄌㄡ'),
                    ('liu', 'ㄌㄧㄡ'),
                    ('lin', 'ㄌㄧㄣ'),
                    ('lie', 'ㄌㄧㄝ'),
                    ('lia', 'ㄌㄧㄚ'),
                    ('lei', 'ㄌㄟ'),
                    ('lao', 'ㄌㄠ'),
                    ('lan', 'ㄌㄢ'),
                    ('lai', 'ㄌㄞ'),
                    ('kuo', 'ㄎㄨㄛ'),
                    ('kun', 'ㄎㄨㄣ'),
                    ('kui', 'ㄎㄨㄟ'),
                    ('kua', 'ㄎㄨㄚ'),
                    ('kou', 'ㄎㄡ'),
                    ('ken', 'ㄎㄣ'),
                    ('kao', 'ㄎㄠ'),
                    ('kan', 'ㄎㄢ'),
                    ('kai', 'ㄎㄞ'),
                    ('jun', 'ㄐㄩㄣ'),
                    ('jue', 'ㄐㄩㄝ'),
                    ('jiu', 'ㄐㄧㄡ'),
                    ('jin', 'ㄐㄧㄣ'),
                    ('jie', 'ㄐㄧㄝ'),
                    ('jia', 'ㄐㄧㄚ'),
                    ('huo', 'ㄏㄨㄛ'),
                    ('hun', 'ㄏㄨㄣ'),
                    ('hui', 'ㄏㄨㄟ'),
                    ('hua', 'ㄏㄨㄚ'),
                    ('hou', 'ㄏㄡ'),
                    ('hen', 'ㄏㄣ'),
                    ('hei', 'ㄏㄟ'),
                    ('hao', 'ㄏㄠ'),
                    ('han', 'ㄏㄢ'),
                    ('hai', 'ㄏㄞ'),
                    ('guo', 'ㄍㄨㄛ'),
                    ('gun', 'ㄍㄨㄣ'),
                    ('gui', 'ㄍㄨㄟ'),
                    ('gua', 'ㄍㄨㄚ'),
                    ('gou', 'ㄍㄡ'),
                    ('gen', 'ㄍㄣ'),
                    ('gei', 'ㄍㄟ'),
                    ('gao', 'ㄍㄠ'),
                    ('gan', 'ㄍㄢ'),
                    ('gai', 'ㄍㄞ'),
                    ('fou', 'ㄈㄡ'),
                    ('fen', 'ㄈㄣ'),
                    ('fei', 'ㄈㄟ'),
                    ('fan', 'ㄈㄢ'),
                    ('eng', 'ㄥ'),
                    ('duo', 'ㄉㄨㄛ'),
                    ('dun', 'ㄉㄨㄣ'),
                    ('dui', 'ㄉㄨㄟ'),
                    ('dou', 'ㄉㄡ'),
                    ('diu', 'ㄉㄧㄡ'),
                    ('die', 'ㄉㄧㄝ'),
                    ('dei', 'ㄉㄟ'),
                    ('dao', 'ㄉㄠ'),
                    ('dan', 'ㄉㄢ'),
                    ('dai', 'ㄉㄞ'),
                    ('cuo', 'ㄘㄨㄛ'),
                    ('cun', 'ㄘㄨㄣ'),
                    ('cui', 'ㄘㄨㄟ'),
                    ('cou', 'ㄘㄡ'),
                    ('chu', 'ㄔㄨ'),
                    ('chi', 'ㄔ'),
                    ('che', 'ㄔㄜ'),
                    ('cha', 'ㄔㄚ'),
                    ('cen', 'ㄘㄣ'),
                    ('cao', 'ㄘㄠ'),
                    ('can', 'ㄘㄢ'),
                    ('cai', 'ㄘㄞ'),
                    ('bin', 'ㄅㄧㄣ'),
                    ('bie', 'ㄅㄧㄝ'),
                    ('ben', 'ㄅㄣ'),
                    ('bei', 'ㄅㄟ'),
                    ('bao', 'ㄅㄠ'),
                    ('ban', 'ㄅㄢ'),
                    ('bai', 'ㄅㄞ'),
                    ('ang', 'ㄤ'),
                    ('zu', 'ㄗㄨ'),
                    ('zi', 'ㄗ'),
                    ('ze', 'ㄗㄜ'),
                    ('za', 'ㄗㄚ'),
                    ('yu', 'ㄩ'),
                    ('yo', 'ㄧㄛ'),
                    ('yi', 'ㄧ'),
                    ('ye', 'ㄧㄝ'),
                    ('ya', 'ㄧㄚ'),
                    ('xu', 'ㄒㄩ'),
                    ('xi', 'ㄒㄧ'),
                    ('wu', 'ㄨ'),
                    ('wo', 'ㄨㄛ'),
                    ('wa', 'ㄨㄚ'),
                    ('tu', 'ㄊㄨ'),
                    ('ti', 'ㄊㄧ'),
                    ('te', 'ㄊㄜ'),
                    ('ta', 'ㄊㄚ'),
                    ('su', 'ㄙㄨ'),
                    ('si', 'ㄙ'),
                    ('se', 'ㄙㄜ'),
                    ('sa', 'ㄙㄚ'),
                    ('ru', 'ㄖㄨ'),
                    ('ri', 'ㄖ'),
                    ('re', 'ㄖㄜ'),
                    ('qu', 'ㄑㄩ'),
                    ('qi', 'ㄑㄧ'),
                    ('pu', 'ㄆㄨ'),
                    ('po', 'ㄆㄛ'),
                    ('pi', 'ㄆㄧ'),
                    ('pa', 'ㄆㄚ'),
                    ('ou', 'ㄡ'),
                    ('nü', 'ㄋㄩ'),
                    ('nu', 'ㄋㄨ'),
                    ('ni', 'ㄋㄧ'),
                    ('ne', 'ㄋㄜ'),
                    ('na', 'ㄋㄚ'),
                    ('mu', 'ㄇㄨ'),
                    ('mo', 'ㄇㄛ'),
                    ('mi', 'ㄇㄧ'),
                    ('me', 'ㄇㄜ'),
                    ('ma', 'ㄇㄚ'),
                    ('lü', 'ㄌㄩ'),
                    ('lu', 'ㄌㄨ'),
                    ('li', 'ㄌㄧ'),
                    ('le', 'ㄌㄜ'),
                    ('la', 'ㄌㄚ'),
                    ('ku', 'ㄎㄨ'),
                    ('ke', 'ㄎㄜ'),
                    ('ka', 'ㄎㄚ'),
                    ('ju', 'ㄐㄩ'),
                    ('ji', 'ㄐㄧ'),
                    ('hu', 'ㄏㄨ'),
                    ('he', 'ㄏㄜ'),
                    ('ha', 'ㄏㄚ'),
                    ('gu', 'ㄍㄨ'),
                    ('ge', 'ㄍㄜ'),
                    ('ga', 'ㄍㄚ'),
                    ('fu', 'ㄈㄨ'),
                    ('fo', 'ㄈㄛ'),
                    ('fa', 'ㄈㄚ'),
                    ('er', 'ㄦ'),
                    ('en', 'ㄣ'),
                    ('ei', 'ㄟ'),
                    ('du', 'ㄉㄨ'),
                    ('di', 'ㄉㄧ'),
                    ('de', 'ㄉㄜ'),
                    ('da', 'ㄉㄚ'),
                    ('cu', 'ㄘㄨ'),
                    ('ci', 'ㄘ'),
                    ('ce', 'ㄘㄜ'),
                    ('ca', 'ㄘㄚ'),
                    ('bu', 'ㄅㄨ'),
                    ('bo', 'ㄅㄛ'),
                    ('bi', 'ㄅㄧ'),
                    ('ba', 'ㄅㄚ'),
                    ('ao', 'ㄠ'),
                    ('an', 'ㄢ'),
                    ('ai', 'ㄞ'),
                    ('o', 'ㄛ'),
                    ('e', 'ㄜ'),
                    ('a', 'ㄚ'),
                    ('5', '˙'),
                    ('4', 'ˋ'),
                    ('3', 'ˇ'),
                    ('2', 'ˊ'),
                    ('1', '')]
