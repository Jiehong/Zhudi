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

import os
import sys
import argparse

import data
import gui

# Parse arguments/definitions
parser = argparse.ArgumentParser(description='Provide a graphical interface'+
                                 ' for *.u8 dictionaries (CEDICT, CFDICT…)')
parser.add_argument("-s", "--split", dest="filename", help="The *.u8"+
                    " dictionary file to be split. This operation will be"+
                    " done in the current directory.")
parser.add_argument("-p", "--pinyin-file", dest="pinyin_file_name", help=
                    "The file that contains the pinyin. This file comes from"+
                    " the split of the *.u8 dictionary file.")
parser.add_argument("-z", "--zhuyin-file", dest="zhuyin_file_name", help=
                    "The file that contains the zhuyin. This file comes from"+
                    " the split of the *.u8 dictionary file.")
parser.add_argument("-tr", "--translation-file", dest="translation_file_name",
                    help="The file that contains the translation. This file"+
                    " comes from the split of the *.u8 dictionary file.")
parser.add_argument("-td", "--traditional-file", dest="traditional_file_name",
                    help="The file that contains the traditional form of the"+
                    " Chinese. This file comes from the split of the *.u8"+
                    " dictionary file.")
parser.add_argument("-sd", "--simplified-file", dest="simplified_file_name",
                    help="The file that contains the simplified form of the"+
                    " Chinese. This file comes from the split of the *.u8"+
                    " dictionary file.")

def split(dictname):
  """
  This function aims to load the *.u8 file and split it.
  """
  dictionary = dictname
  # Open the dictionary in text mode, read only
  with open(dictionary,mode="r") as dic:
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

    if i[0] !="#":
      for k in range(len(i)):
        if i[k] == " ": # look  for spaces
          space_ind.append(k)
        if i[k] =="[": # look for pinyin delimiters
          pinyin_delimiters.append(k)
        if i[k] =="]":
          pinyin_delimiters.append(k)
        if i[k] == "/": # look for translation delimiters
          translation_delimiters.append(k)
      traditional = i[0:space_ind[0]]
      simplified = i[space_ind[0]+1:space_ind[1]]
      pinyin = i[pinyin_delimiters[0]+1:pinyin_delimiters[1]]
      for n in range(len(translation_delimiters)-1):
        translation.append(i[translation_delimiters[n]+1:translation_delimiters[n+1]])
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
      
  return (simplified_list,
          traditional_list,
          translation_list,
          pinyin_list)
# End of split()

# Read files and defaults values
def read_files(pinyin_file_name,
               zhuyin_file_name,
               simplified_file_name,
               traditional_file_name,
               translation_file_name):
  try:
    pinyin_file = open(pinyin_file_name,"r")
    pinyin = pinyin_file.readlines()
    pinyin_file.close
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

def main():
  options = parser.parse_args()
  filename = options.filename
  pinyin_file_name=options.pinyin_file_name
  zhuyin_file_name=options.zhuyin_file_name
  simplified_file_name=options.simplified_file_name
  translation_file_name=options.translation_file_name
  traditional_file_name=options.traditional_file_name
  if (filename == None) and (pinyin_file_name is not None and zhuyin_file_name is not None and simplified_file_name is not None and traditional_file_name is not None and translation_file_name is not None):
    pinyin, zhuyin, traditional, simplified, translation = read_files(
      pinyin_file_name,
      zhuyin_file_name,
      simplified_file_name,
      traditional_file_name,
      translation_file_name)
    # Default values
    language = "Chinese"
    romanisation = "Zhuyin"
    hanzi = "Traditional"
    myData = data.Dictionary(simplified, traditional, translation, pinyin, zhuyin)
    
    global mw
    mw = gui.main_window(myData)
    mw.hanzi = hanzi
    mw.romanisation = romanisation
    mw.language = language
    mw.build()
    mw.loop()
    
  if (filename is not None) and (pinyin_file_name is None and zhuyin_file_name is None and simplified_file_name is None and traditional_file_name is None and translation_file_name is None):
    print("Splitting dictionary in progress…")
    files = split(filename)
    simplified_list = files[0]
    traditional_list = files[1]
    translation_list = files[2]
    pinyin_list = files[3]
    
    myData = data.Dictionary(simplified_list,
                             traditional_list,
                             translation_list,
                             pinyin_list)
    print(" Pinyin to Zhuyin conversion in progress…")
    myData.pinyin_to_zhuyin()
    print("done.")
  if (filename is None) and (pinyin_file_name is None and zhuyin_file_name is None and simplified_file_name is None and traditional_file_name is None and translation_file_name is None):
    parser.print_help()
# end of main

# Launching!
if __name__ == "__main__":
  main()
