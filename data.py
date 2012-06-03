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
import re

import pinyin_to_zhuyin_table as pz

class Dictionary ():
  """
  This class aims to contain data and methods to convert, serach them.
  """
  def __init__(self, a, b, c, d, e=[]):
    self.simplified = a
    self.traditional = b
    self.translation = c
    self.pinyin = d
    self.zhuyin = e
    self.index_list = []

  def pinyin_to_zhuyin(self):
    """
    This function converts the pinyin list attribute into zhuyin and saves
    it into the zhuyin attribute of the Data class.
    """
    pinyin_zhuyin_dict = pz.pinyin_to_zhuyin

    # for speed issue, transforme the list of pinyin in one long string
    to_convert = " " + " # ".join(self.pinyin)
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
    # Break the long string as a list and save it
    zhuyin = zhuyin.split(" # ")
    zhuyin[0] = zhuyin[0][1:] # get rid of the first space
    self.zhuyin = zhuyin
    with open("zhuyin", mode="w") as zhuyin_file:
      for line in zhuyin:
        zhuyin_file.write(line+"\n")

  def search(self, given_list, text):
    """
    Given a list and a text, this function saves the list of indices in
    the index_list attribute of the Data class.
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
    self.index_list = index

  def get_data_at_index(self, index):
    """
    This function returns all the data (in a tuple) at the given index.
    """
    return (self.simplified[index],
            self.traditional[index],
            self.translation[index],
            self.pinyin[index],
            self.zhuyin[index])
