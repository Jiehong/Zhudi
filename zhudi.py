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

#!/usr/bin/env python
import re
import os
import sys
import argparse
from gi.repository import Gtk, Pango

# Parse arguments/definitions
parser = argparse.ArgumentParser(description='Provide a graphical interface'+
                                 ' for *.u8 dictionaries (CEDICT, CFDICT…)')
parser.add_argument("-s", "--split", dest="filename", help="The *.u8"+
                    " dictionary file to be split. This operation will be done"+
                    " in the current directory.")
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


# Preprocessing of the *.u8
def Preprocessing(dictname):
    """
    This function aims to load proper files and to translate pinyin into
    zhuyin.
    """
    dictionary = dictname
    # Open the dictionary in text mode, read only
    with open(dictionary,mode="r") as dic:
        liste = dic.readlines() # Use the text file as lines
    dic.closed
    space_ind = []
    pinyin_delimiters = []
    translation_delimiters = []
    translation = []
    zhuyin = []
    # Pinyin/zhuyin conversion table
    pin_dict = ["zhuang","shuang","chuang","zhuan","zhuai","zhong","zheng","zhang","xiong","xiang","shuan","shuai","sheng","shang","qiong","qiang","niang","liang","kuang","jiong","jiang","huang","guang","chuan","chuai","chong","cheng","chang","zuan","zong","zhuo","zhun","zhui","zhua","zhou","zhen","zhei","zhao","zhan","zhai","zeng","zang","yuan","yong","ying","yang","xuan","xing","xien","xiao","xian","wong","weng","wang","tuan","tong","ting","tien","tiao","tian","teng","tang","suan","song","shuo","shun","shui","shua","shou","shen","shei","shao","shan","shai","seng","sang","ruan","rong","reng","rang","quan","qing","qien","qiao","qian","ping","pien","piao","pian","peng","pang","nuan","nong","ning","nien","niao","nian","neng","nang","ming","mien","miao","mian","meng","mang","luen","luan","long","ling","lien","liao","lian","leng","lang","kuan","kuai","kong","keng","kang","juan","jing","jien","jiao","jian","huan","huai","hong","heng","hang","guan","guai","gong","geng","gang","fong","fiao","feng","fang","duan","dong","ding","dien","diao","dian","deng","dang","cuan","cong","chuo","chun","chui","chua","chou","chen","chao","chan","chai","ceng","cang","bing","bien","biao","bian","beng","bang","zuo","zun","zui","zou","zhu","zhi","zhe","zha","zen","zei","zao","zan","zai","yun","yue","you","yin","yao","yan","yai","xun","xue","xiu","xin","xie","xia","wen","wei","wan","wai","tuo","tun","tui","tou","tie","tao","tan","tai","suo","sun","sui","sou","shu","shi","she","sha","sen","sei","sao","san","sai","ruo","run","rui","rou","ren","rao","ran","qun","que","qiu","qin","qie","qia","pou","pin","pie","pen","pei","pao","pan","pai","nuo","nüe","nou","niu","nin","nie","nen","nei","nao","nan","nai","mou","miu","min","mie","men","mei","mao","man","mai","luo","lun","lüe","lou","liu","lin","lie","lia","lei","lao","lan","lai","kuo","kun","kui","kua","kou","ken","kao","kan","kai","jun","jue","jiu","jin","jie","jia","huo","hun","hui","hua","hou","hen","hei","hao","han","hai","guo","gun","gui","gua","gou","gen","gei","gao","gan","gai","fou","fen","fei","fan","eng","duo","dun","dui","dou","diu","die","dei","dao","dan","dai","cuo","cun","cui","cou","chu","chi","che","cha","cen","cao","can","cai","bin","bie","ben","bei","bao","ban","bai","ang","zu","zi","ze","za","yu","yo","yi","ye","ya","xu","xi","wu","wo","wa","tu","ti","te","ta","su","si","se","sa","ru","ri","re","qu","qi","pu","po","pi","pa","ou","nü","nu","ni","ne","na","mu","mo","mi","me","ma","lü","lu","li","le","la","ku","ke","ka","ju","ji","hu","he","ha","gu","ge","ga","fu","fo","fa","er","en","ei","du","di","de","da","cu","ci","ce","ca","bu","bo","bi","ba","ao","an","ai","o","e","a","5","4","3","2","1"]
    zhu_dict = ["ㄓㄨㄤ","ㄕㄨㄤ","ㄔㄨㄤ","ㄓㄨㄢ","ㄓㄨㄞ","ㄓㄨㄥ","ㄓㄥ","ㄓㄤ","ㄒㄩㄥ","ㄒㄧㄤ","ㄕㄨㄢ","ㄕㄨㄞ","ㄕㄥ","ㄕㄤ","ㄑㄩㄥ","ㄑㄧㄤ","ㄋㄧㄤ","ㄌㄧㄤ","ㄎㄨㄤ","ㄐㄩㄥ","ㄐㄧㄤ","ㄏㄨㄤ","ㄍㄨㄤ","ㄔㄨㄢ","ㄔㄨㄞ","ㄔㄨㄥ","ㄔㄥ","ㄔㄤ","ㄗㄨㄢ","ㄗㄨㄥ","ㄓㄨㄛ","ㄓㄨㄣ","ㄓㄨㄟ","ㄓㄨㄚ","ㄓㄡ","ㄓㄣ","ㄓㄟ","ㄓㄠ","ㄓㄢ","ㄓㄞ","ㄗㄥ","ㄗㄤ","ㄩㄢ","ㄩㄥ","ㄧㄥ","ㄧㄤ","ㄒㄩㄢ","ㄒㄧㄥ","ㄒㄧㄢ","ㄒㄧㄠ","ㄒㄧㄢ","ㄨㄥ","ㄨㄥ","ㄨㄤ","ㄊㄨㄢ","ㄊㄨㄥ","ㄊㄧㄥ","ㄊㄧㄢ","ㄊㄧㄠ","ㄊㄧㄢ","ㄊㄥ","ㄊㄤ","ㄙㄨㄢ","ㄙㄨㄥ","ㄕㄨㄛ","ㄕㄨㄣ","ㄕㄨㄟ","ㄕㄨㄚ","ㄕㄡ","ㄕㄣ","ㄕㄟ","ㄕㄠ","ㄕㄢ","ㄕㄞ","ㄙㄥ","ㄙㄤ","ㄖㄨㄢ","ㄖㄨㄥ","ㄖㄥ","ㄖㄤ","ㄑㄩㄢ","ㄑㄧㄥ","ㄑㄧㄢ","ㄑㄧㄠ","ㄑㄧㄢ","ㄆㄧㄥ","ㄆㄧㄢ","ㄆㄧㄠ","ㄆㄧㄢ","ㄆㄥ","ㄆㄤ","ㄋㄨㄢ","ㄋㄨㄥ","ㄋㄧㄥ","ㄋㄧㄢ","ㄋㄧㄠ","ㄋㄧㄢ","ㄋㄥ","ㄋㄤ","ㄇㄧㄥ","ㄇㄧㄢ","ㄇㄧㄠ","ㄇㄧㄢ","ㄇㄥ","ㄇㄤ","ㄌㄩㄢ","ㄌㄨㄢ","ㄌㄨㄥ","ㄌㄧㄥ","ㄌㄧㄢ","ㄌㄧㄠ","ㄌㄧㄢ","ㄌㄥ","ㄌㄤ","ㄎㄨㄢ","ㄎㄨㄞ","ㄎㄨㄥ","ㄎㄥ","ㄎㄤ","ㄐㄩㄢ","ㄐㄧㄥ","ㄐㄧㄢ","ㄐㄧㄠ","ㄐㄧㄢ","ㄏㄨㄢ","ㄏㄨㄞ","ㄏㄨㄥ","ㄏㄥ","ㄏㄤ","ㄍㄨㄢ","ㄍㄨㄞ","ㄍㄨㄥ","ㄍㄥ","ㄍㄤ","ㄈㄨㄥ","ㄈㄧㄠ","ㄈㄥ","ㄈㄤ","ㄉㄨㄢ","ㄉㄨㄥ","ㄉㄧㄥ","ㄉㄧㄢ","ㄉㄧㄠ","ㄉㄧㄢ","ㄉㄥ","ㄉㄤ","ㄘㄨㄢ","ㄘㄨㄥ","ㄔㄨㄛ","ㄔㄨㄣ","ㄔㄨㄟ","ㄔㄨㄚ","ㄔㄡ","ㄔㄣ","ㄔㄠ","ㄔㄢ","ㄔㄞ","ㄘㄥ","ㄘㄤ","ㄅㄧㄥ","ㄅㄧㄢ","ㄅㄧㄠ","ㄅㄧㄢ","ㄅㄥ","ㄅㄤ","ㄗㄨㄛ","ㄗㄨㄣ","ㄗㄨㄟ","ㄗㄡ","ㄓㄨ","ㄓ","ㄓㄜ","ㄓㄚ","ㄗㄣ","ㄗㄟ","ㄗㄠ","ㄗㄢ","ㄗㄞ","ㄩㄣ","ㄩㄝ","ㄧㄡ","ㄧㄣ","ㄧㄠ","ㄧㄢ","ㄧㄞ","ㄒㄩㄣ","ㄒㄩㄝ","ㄒㄧㄡ","ㄒㄧㄣ","ㄒㄧㄝ","ㄒㄧㄚ","ㄨㄣ","ㄨㄟ","ㄨㄢ","ㄨㄞ","ㄊㄨㄛ","ㄊㄨㄣ","ㄊㄨㄟ","ㄊㄡ","ㄊㄧㄝ","ㄊㄠ","ㄊㄢ","ㄊㄞ","ㄙㄨㄛ","ㄙㄨㄣ","ㄙㄨㄟ","ㄙㄡ","ㄕㄨ","ㄕ","ㄕㄜ","ㄕㄚ","ㄙㄣ","ㄙㄟ","ㄙㄠ","ㄙㄢ","ㄙㄞ","ㄖㄨㄛ","ㄖㄨㄣ","ㄖㄨㄟ","ㄖㄡ","ㄖㄣ","ㄖㄠ","ㄖㄢ","ㄑㄩㄣ","ㄑㄩㄝ","ㄑㄧㄡ","ㄑㄧㄣ","ㄑㄧㄝ","ㄑㄧㄚ","ㄆㄡ","ㄆㄧㄣ","ㄆㄧㄝ","ㄆㄣ","ㄆㄟ","ㄆㄠ","ㄆㄢ","ㄆㄞ","ㄋㄨㄛ","ㄋㄩㄝ","ㄋㄡ","ㄋㄧㄡ","ㄋㄧㄣ","ㄋㄧㄝ","ㄋㄣ","ㄋㄟ","ㄋㄠ","ㄋㄢ","ㄋㄞ","ㄇㄡ","ㄇㄧㄡ","ㄇㄧㄣ","ㄇㄧㄝ","ㄇㄣ","ㄇㄟ","ㄇㄠ","ㄇㄢ","ㄇㄞ","ㄌㄨㄛ","ㄌㄨㄣ","ㄌㄩㄝ","ㄌㄡ","ㄌㄧㄡ","ㄌㄧㄣ","ㄌㄧㄝ","ㄌㄧㄚ","ㄌㄟ","ㄌㄠ","ㄌㄢ","ㄌㄞ","ㄎㄨㄛ","ㄎㄨㄣ","ㄎㄨㄟ","ㄎㄨㄚ","ㄎㄡ","ㄎㄣ","ㄎㄠ","ㄎㄢ","ㄎㄞ","ㄐㄩㄣ","ㄐㄩㄝ","ㄐㄧㄡ","ㄐㄧㄣ","ㄐㄧㄝ","ㄐㄧㄚ","ㄏㄨㄛ","ㄏㄨㄣ","ㄏㄨㄟ","ㄏㄨㄚ","ㄏㄡ","ㄏㄣ","ㄏㄟ","ㄏㄠ","ㄏㄢ","ㄏㄞ","ㄍㄨㄛ","ㄍㄨㄣ","ㄍㄨㄟ","ㄍㄨㄚ","ㄍㄡ","ㄍㄣ","ㄍㄟ","ㄍㄠ","ㄍㄢ","ㄍㄞ","ㄈㄡ","ㄈㄣ","ㄈㄟ","ㄈㄢ","ㄥ","ㄉㄨㄛ","ㄉㄨㄣ","ㄉㄨㄟ","ㄉㄡ","ㄉㄧㄡ","ㄉㄧㄝ","ㄉㄟ","ㄉㄠ","ㄉㄢ","ㄉㄞ","ㄘㄨㄛ","ㄘㄨㄣ","ㄘㄨㄟ","ㄘㄡ","ㄔㄨ","ㄔ","ㄔㄜ","ㄔㄚ","ㄘㄣ","ㄘㄠ","ㄘㄢ","ㄘㄞ","ㄅㄧㄣ","ㄅㄧㄝ","ㄅㄣ","ㄅㄟ","ㄅㄠ","ㄅㄢ","ㄅㄞ","ㄤ","ㄗㄨ","ㄗ","ㄗㄜ","ㄗㄚ","ㄩ","ㄧㄛ","ㄧ","ㄧㄝ","ㄧㄚ","ㄒㄩ","ㄒㄧ","ㄨ","ㄨㄛ","ㄨㄚ","ㄊㄨ","ㄊㄧ","ㄊㄜ","ㄊㄚ","ㄙㄨ","ㄙ","ㄙㄜ","ㄙㄚ","ㄖㄨ","ㄖ","ㄖㄜ","ㄑㄩ","ㄑㄧ","ㄆㄨ","ㄆㄛ","ㄆㄧ","ㄆㄚ","ㄡ","ㄋㄩ","ㄋㄨ","ㄋㄧ","ㄋㄜ","ㄋㄚ","ㄇㄨ","ㄇㄛ","ㄇㄧ","ㄇㄜ","ㄇㄚ","ㄌㄩ","ㄌㄨ","ㄌㄧ","ㄌㄜ","ㄌㄚ","ㄎㄨ","ㄎㄜ","ㄎㄚ","ㄐㄩ","ㄐㄧ","ㄏㄨ","ㄏㄜ","ㄏㄚ","ㄍㄨ","ㄍㄜ","ㄍㄚ","ㄈㄨ","ㄈㄛ","ㄈㄚ","ㄦ","ㄣ","ㄟ","ㄉㄨ","ㄉㄧ","ㄉㄜ","ㄉㄚ","ㄘㄨ","ㄘ","ㄘㄜ","ㄘㄚ","ㄅㄨ","ㄅㄛ","ㄅㄧ","ㄅㄚ","ㄠ","ㄢ","ㄞ","ㄛ","ㄜ","ㄚ","˙","ˋ","ˇ","ˊ"," "]
    # Spliting list of the dictionary
    pinyin_file = open("pinyin","a")
    traditional_file = open("traditional","a")
    simplified_file = open("simplified","a")
    translation_file = open("translation","a")
    zhuyin_file = open("zhuyin","a")

    for i in liste: # for each line
        del space_ind[:]
        del pinyin_delimiters[:]
        del translation_delimiters[:]
        del translation[:]
	
        if i[0] !="#":
            for k in range(len(i)):
                if i[k] == " ": # look  for spaces
                    space_ind.append(k)
                if i[k] =="[": # look for pinyin delimiters
                    pinyin_delimiters.append(k)
                if i[k] =="]":
                    pinyin_delimiters.append(k)
                if i[k] == "/": # look for translation delimiters: /meaning 1/meaning 2/
                    translation_delimiters.append(k)
            traditional = i[0:space_ind[0]]
            simplified = i[space_ind[0]+1:space_ind[1]]
            pinyin = i[pinyin_delimiters[0]+1:pinyin_delimiters[1]] # works even if the pinyin field is empty
            for n in range(len(translation_delimiters)-1):
                translation.append(i[translation_delimiters[n]+1:translation_delimiters[n+1]])
            # Get rid of sticking pinyin like di4shang4 instead of di4 shang4
            clean_pinyin = ""
            for n in range(len(pinyin)):
                clean_pinyin += pinyin[n]
                if pinyin[n].isdigit() and (n < len(pinyin)-1):
                    if pinyin[n+1] != " ":
                        clean_pinyin += " "
                        
            pinyin_file.write(clean_pinyin)
            pinyin_file.write("\n")
            traditional_file.write(traditional)
            traditional_file.write("\n")
            simplified_file.write(simplified)
            simplified_file.write("\n")
            for i in range(len(translation)):
                if i != 0:
                    translation_file.write("$")
                translation_file.write(translation[i])
            translation_file.write("\n")
            zhuyin.append(" "+clean_pinyin.lower()+" ")
    # Convert the list of zhuyin line in one long string and use regular expressions
    zhuyin = '#'.join(zhuyin)
    zhuyin = re.sub("u:","ü",zhuyin)	# change u: into ü
    zhuyin = re.sub(" r "," er ",zhuyin)	# change r into er
    for i in range(len(pin_dict)):
        if i < len(pin_dict)-5:
            zhuyin = re.sub(" "+pin_dict[i]," "+zhu_dict[i],zhuyin)   # do not change the tones
        if i >= len(pin_dict)-5:
            zhuyin = re.sub(pin_dict[i]+" |$",zhu_dict[i]+" ",zhuyin) # tones
    # Change the result as a list and save it
    zhuyin = zhuyin.split("#")
    for line in zhuyin:
        zhuyin_file.write(line)
        zhuyin_file.write("\n")
        
        traditional_file.closed
        simplified_file.closed
        translation_file.closed
        pinyin_file.closed
        zhuyin_file.closed
# End of Preprocessing()

# Read files and defaults values
def read_files(pinyin_file_name,zhuyin_file_name,simplified_file_name,traditional_file_name,translation_file_name):
    global pinyin
    global zhuyin
    global traditional
    global simplified
    global translation
    global language
    global romanisation
    global hanzi
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
    except(IOError) as errno:
        print("### The dictionary files couldn't be read. Make sure you have split the dictonary file first. ###")
        quit()
    # Defaults values
    language = "Chinese"
    romanisation = "Zhuyin"
    hanzi = "Traditional"
# End of read_files()
	
# Functions
def set_language(lang):
    global language # Use the value of that variable somewhere else
    language = lang

def display_translation(index,language):
    global translation
    global traditional
    global zhuyin
    global pinyin
    global romanisation
    global simplified
	
    if hanzi == "Traditional":
        hanzi_dic = traditional
    else:
        hanzi_dic = simplified
	
    if romanisation == "Zhuyin":
        romanisation_dic = zhuyin
    else:
        romanisation_dic = pinyin
    tr = mw.translation_box.get_buffer()
    dollars_list = []
    t = translation[index]
    for l in range(len(t)):
        if t[l] == "$":
            dollars_list.append(l)
    temp = 0
    trans = []
    for k in range(len(dollars_list)):
        trans.append(str(k+1)+". "+t[temp:dollars_list[k]])
        temp = dollars_list[k]+1
    trans.append(str(len(dollars_list)+1)+". "+t[temp:len(t)])
    string = ""
    for i in range(len(dollars_list)+1):
        string = string + trans[i]+"\n"

    # Add [] arround the pronounciation parts
    p_string = romanisation_dic[index].split()
    pronounciation_string = []
    for point in range(len(p_string)):
        pronounciation_string.append("[")
        pronounciation_string.append(p_string[point])
        pronounciation_string.append("]")
    # pronounciation_string = p_string
    tr.set_text("Chinese\n"+hanzi_dic[index]+"\n\n"+"Pronunciation\n"+''.join(pronounciation_string)+"\n\nMeaning\n"+string) # Display in the Translation box
    bold = tr.create_tag(weight=Pango.Weight.BOLD)
    big = tr.create_tag(size=30*Pango.SCALE)
    medium = tr.create_tag(size=15*Pango.SCALE)
    blue = tr.create_tag(foreground="blue")
	
    # "Chinese" in bold
    start_1 = tr.get_iter_at_line(0)
    end_1 = tr.get_iter_at_line(0)
    end_1.forward_to_line_end()
    tr.apply_tag(bold, start_1, end_1)
	
    # Bigger Chinese
    start_c = tr.get_iter_at_line(1)
    end_c = tr.get_iter_at_line(1)
    end_c.forward_to_line_end()
    tr.apply_tag(big, start_c, end_c)
	
    # "Pronunciation" in bold
    start_2 = tr.get_iter_at_line(4)
    end_2 = tr.get_iter_at_line(4)
    end_2.forward_to_line_end()
    tr.apply_tag(bold, start_2, end_2)
	
    # "Pronunciation" in blue
    start_3 = tr.get_iter_at_line(5)
    end_3 = tr.get_iter_at_line(5)
    end_3.forward_to_line_end()
    tr.apply_tag(blue, start_3, end_3)
    tr.apply_tag(medium,start_3, end_3)
	
    # "Meaning" in bold
    start_3 = tr.get_iter_at_line(7)
    end_3 = tr.get_iter_at_line(7)
    end_3.forward_to_line_end()
    tr.apply_tag(bold, start_3, end_3)
# End of display_translation
    
def find_Text(liste,text):
    # Look for merely matching
    words = (text.lower()).split()
    index = []
    total = []
    for k in range(len(liste)): # try in each line of the dic
        counter = 0
        for s in range(len(words)): # for each word of the request (case insensitive)
            if (liste[k].lower()).count(words[s]) != 0:
                counter = counter +1
            if counter == len(words): # only accepts lines containing every words
                index.append(k)
                total.append(len(liste[k]))
    d = dict(zip(index,total))
    dl = sorted(d.items(), key=lambda x: x[1])
    index = []
    for i in range(len(dl)): # Keep the sorted results
        index.append(dl[i][0])
    return index
# end of find_Text
			
def search(searchfield, which):
    global translation
    global traditional
    global language
    global hanzi
    global search_index
	
    w = 40	
    if hanzi == "Traditional":
        hanzi_dic = traditional
    else:
        hanzi_dic = simplified
    if language == "Latin":
        dic = translation
        dic2 = hanzi_dic
    else:
        dic = hanzi_dic
       	dic2 = translation
    text = searchfield.get_text()
    tr = mw.translation_box.get_buffer()

    # First case: the text has already been searched (just before) (i.e. the result is not the first one)
    if which != 0:
        display_translation(search_index[which],language)
    else: # Second case: the result is the first one (i.e. it has been selected or it's a new search (by default))
        mw.results_list.clear()
        if len(text) == 0: # If no text to look for (breaking an infinite loop)
            tr.set_text("Nothing found.")
            mw.results_list.append(["Nothing to look for…"])
        else: # If the search area isn't empty, just search for it!
            search_index = find_Text(dic,text)
            if len(search_index) == 0:
                tr.set_text("No results found.")
                mw.results_list.append(["No results found."])
            else: # Display of the first result and its translation
                display_translation(search_index[which],language)
                if len(dic[search_index[0]]) > w:
                    mw.results_list.append(["1. " + dic[search_index[0]][0:w-1]+"…"])
                else:
                    mw.results_list.append(["1. " + dic[search_index[0]][0:len(dic[search_index[0]])-1]])			
            if len(search_index) > 1:
                for k in range(len(search_index)-1):
                    if len(dic[search_index[k+1]]) > w:
                        mw.results_list.append([str(k+2) + ". " + dic[search_index[k+1]][0:w-1]+"…"])
                    else:
                        mw.results_list.append([str(k+2) + ". " + dic[search_index[k+1]][0:len(dic[search_index[k+1]])-1]])
# end of search

def set_hanzi(han):
    global hanzi
    hanzi = han

def set_romanisation(rom):
    global romanisation
    romanisation = rom

def results_changed(selection,searchfield):
    if selection is not None:
        model, treeiter = selection.get_selected()
        till = 0
        what = []
        while what != ".":
            what = model[treeiter][0][till]
            till = till + 1
        which = int(model[treeiter][0][0:till-1])-1
        search(searchfield,which)
	
class option_window:
    def kill_ok(self):
        self.window.hide()

    def __init__(self):
        # Definition of the options window
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_size_request(300,180)
        self.window.set_title("Options")
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.connect("destroy", lambda x:self.window.destroy)
		
        # Hanzi label
        hanzi_label = Gtk.Label()
        hanzi_label.set_text("<big>Chinese characters form:</big>")
        hanzi_label.set_justify(Gtk.Justification.LEFT)
        hanzi_label.set_use_markup(True)
		
        # hanzi box
        hanzi_box = Gtk.Grid()
        Traditional = Gtk.RadioButton.new_with_label_from_widget(None,"Traditional")
        Traditional.connect("clicked", lambda x: set_hanzi("Traditional"))
        hanzi_box.add(Traditional)
        Simplified = Gtk.RadioButton.new_with_label_from_widget(Traditional,"Simplified")
        Simplified.connect("clicked", lambda x: set_hanzi("Simplified"))
        hanzi_box.attach_next_to(Simplified,Traditional,Gtk.PositionType.RIGHT,1,1)
        hanzi_box.set_column_homogeneous(True)

        if hanzi == "Traditional":
            Traditional.set_active(True)
        else:
            Simplified.set_active(True)
		
        # Romanisation label
        romanisation_label = Gtk.Label()
        romanisation_label.set_text("<big>Pronunciation system:</big>")
        romanisation_label.set_justify(Gtk.Justification.LEFT)
        romanisation_label.set_use_markup(True)
		
        # romanisation box
        romanisation_box = Gtk.Grid()
        Zhu = Gtk.RadioButton.new_with_label_from_widget(None,"Zhuyin Fuhao")
        Zhu.connect("clicked", lambda x: set_romanisation("Zhuyin"))
        romanisation_box.add(Zhu)
        Pin = Gtk.RadioButton.new_with_label_from_widget(Zhu,"Hanyu Pinyin")
        Pin.connect("clicked", lambda x: set_romanisation("Pinyin"))
        romanisation_box.attach_next_to(Pin,Zhu,Gtk.PositionType.RIGHT,1,1)
        if romanisation == "Zhuyin":
            Zhu.set_active(True)
        else:
            Pin.set_active(True)
        romanisation_box.set_column_homogeneous(True)
		
        # Horizontal separator
        option_horizontal_separator = Gtk.Separator()
		
        # Ok button
        ok_button = Gtk.Button("Ok")
        ok_button.connect("clicked", lambda x:self.kill_ok())
        
        # Mapping of the option window
        loption_vertical_box = Gtk.Grid()
        loption_vertical_box.add(hanzi_label)
        loption_vertical_box.attach_next_to(hanzi_box,hanzi_label,Gtk.PositionType.BOTTOM,1,1)
        loption_vertical_box.attach_next_to(romanisation_label,hanzi_box,Gtk.PositionType.BOTTOM,1,1)
        loption_vertical_box.attach_next_to(romanisation_box, romanisation_label,Gtk.PositionType.BOTTOM,1,1)
        loption_vertical_box.attach_next_to(option_horizontal_separator, romanisation_box,Gtk.PositionType.BOTTOM,1,1)
        loption_vertical_box.attach_next_to(ok_button, option_horizontal_separator,Gtk.PositionType.BOTTOM,1,2)
        loption_vertical_box.set_column_homogeneous(True)
        loption_vertical_box.set_row_homogeneous(True)
		
        # Adding them in the main window
        self.window.add(loption_vertical_box)
        
        # Eventually, show the option window and the widgetss
        self.window.show_all()
# End of Option_window

class main_window:
    def open_option(widget,self):
        opt = option_window()

    def __init__(self):		
        # Definition of the main window
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_default_size(800,494) # Gold number ratio
        self.window.set_title("Zhudi")
        self.window.set_position(Gtk.WindowPosition.CENTER)
		
        # Search label
        search_label = Gtk.Label()
        search_label.set_text("<big>Searching area</big>")
        search_label.set_use_markup(True)
		
        # Search field
        search_field = Gtk.Entry()
        search_field.set_visible(True)
        search_field.connect("activate", search,0)
        search_field.set_placeholder_text("Type your search here…")

		
        # Go, search! button
        go_button = Gtk.Button("Search")
        go_button.connect("clicked", lambda x: search(search_field,0))
		
        # Options button
        option_button = Gtk.Button("Options")
        option_button.connect("clicked", self.open_option)
		
        # Search + button box
        SB_box = Gtk.Grid()
        SB_box.attach(search_field,0,0,4,1)
        SB_box.attach_next_to(go_button,search_field,Gtk.PositionType.RIGHT,1,1)
        SB_box.attach_next_to(option_button,go_button,Gtk.PositionType.RIGHT,1,1)
        SB_box.set_column_homogeneous(True)
		
        # Search label zone
        frame_search = Gtk.Frame()
        frame_search.set_label_widget(search_label)
        frame_search.add(SB_box)
		
        # Language box
        language_box = Gtk.Grid()
        Chinese = Gtk.RadioButton.new_with_label_from_widget(None,"From Chinese")
        Chinese.connect("clicked", lambda x: set_language("Chinese"))
        language_box.add(Chinese)
        Latin = Gtk.RadioButton.new_with_label_from_widget(Chinese, "To Chinese")
        Latin.connect("clicked", lambda x: set_language("Latin"))
        language_box.attach_next_to(Latin,Chinese,Gtk.PositionType.RIGHT,1,1)
        language_box.set_column_homogeneous(True)
        Chinese.set_active(True)

        # Results part in a list
        self.results_list = Gtk.ListStore(str)
        results_tree = Gtk.TreeView(self.results_list)
        renderer = Gtk.CellRendererText()
        results_tree.tvcolumn = Gtk.TreeViewColumn("Results", renderer, text=0)
        results_tree.append_column(results_tree.tvcolumn)
        self.results_list.cell = Gtk.CellRendererText()
        results_tree.tvcolumn.pack_start(self.results_list.cell, True)
        results_tree.set_enable_search(False)
        results_tree.tvcolumn.set_sort_column_id(False)
        results_tree.set_reorderable(False)
        results_tree.connect("cursor-changed", lambda x: results_changed(results_tree.get_selection(),search_field))
        
        results_scroll = Gtk.ScrolledWindow()
        results_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) # No horizontal bar, automatic vertical bar
        results_scroll.add_with_viewport(results_tree)
        
        frame_results = Gtk.Frame()
        frame_results.add(results_scroll)
        
        # Translation Label
        translation_label = Gtk.Label()
        translation_label.set_text("<big>Translation</big>")
        translation_label.set_use_markup(True)
		
        # Translation view
        self.translation_box = Gtk.TextView(buffer=None)
        self.translation_box.set_editable(False)
        self.translation_box.set_cursor_visible(False)
        self.translation_box.set_wrap_mode(Gtk.WrapMode.WORD) # No horizontal bar, vertical bar if needed
        tr = self.translation_box.get_buffer()
        bold = tr.create_tag(weight=Pango.Weight.BOLD)
        big = tr.create_tag(size=30*Pango.SCALE)
        medium = tr.create_tag(size=15*Pango.SCALE)
        blue = tr.create_tag(foreground="blue")
		
        translation_scroll = Gtk.ScrolledWindow()
        translation_scroll.add_with_viewport(self.translation_box)
        
        frame_translation = Gtk.Frame()
        frame_translation.set_label_widget(translation_label)
        frame_translation.add(translation_scroll)
        
		
        # Mapping of the main window
        left_vertical_box = Gtk.Grid()
        left_vertical_box.add(frame_search)
        left_vertical_box.attach_next_to(language_box, frame_search,Gtk.PositionType.BOTTOM,1,1)
        left_vertical_box.attach_next_to(frame_results, language_box, Gtk.PositionType.BOTTOM, 1, 7)
        left_vertical_box.set_row_homogeneous(True)
        left_vertical_box.set_column_homogeneous(True)
        
        right_vertical_box = Gtk.Grid()
        right_vertical_box.add(frame_translation)
        right_vertical_box.set_column_homogeneous(True)
        right_vertical_box.set_row_homogeneous(True)
        
        horizontal_box = Gtk.Grid()
        horizontal_box.attach(left_vertical_box,0,0,1,1)
        horizontal_box.attach_next_to(right_vertical_box, left_vertical_box, Gtk.PositionType.RIGHT,1,1)
        horizontal_box.set_column_homogeneous(True)
        horizontal_box.set_row_homogeneous(True)
		
        # Adding them in the main window
        self.window.add(horizontal_box)
        
        self.window.connect("destroy",Gtk.main_quit)
        self.window.show_all()
        
    def loop(self):
        Gtk.main()
# end of main_Window
        
def main():
    options = parser.parse_args()
    filename = options.filename
    pinyin_file_name=options.pinyin_file_name
    zhuyin_file_name=options.zhuyin_file_name
    simplified_file_name=options.simplified_file_name
    traditional_file_name=options.traditional_file_name
    translation_file_name=options.translation_file_name
    if (filename == None) and (pinyin_file_name is not None and zhuyin_file_name is not None and simplified_file_name is not None and traditional_file_name is not None and translation_file_name is not None):
        read_files(pinyin_file_name,zhuyin_file_name,simplified_file_name,traditional_file_name,translation_file_name)
        global mw
        mw = main_window()
        global search_index
        search_index = []
        mw.loop()
    if (filename is not None) and (pinyin_file_name == None and zhuyin_file_name == None and simplified_file_name == None and traditional_file_name == None and translation_file_name == None):
        print("Splitting the dictionary in progress…")
        Preprocessing(filename)
        print("done.")
    else:
        parser.print_help()
# end of main

main()
