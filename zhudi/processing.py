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

import re
import os
import shutil


class PreProcessing(object):
    """ This class is in charge of the pre-processing needed to lauch Zhudi.
    It loads config files, split dictionaries, etc.
    """

    def __init__(self):
        pass

    def split(self, dictname):
        """ Loads the *.u8 file and split it. Return a tuple of 4 lists:
        (simplified_list,
        traditional_list,
        translation_list,
        pinyin_list)
        """

        def unStick(pinyin):
            """ Get rid of sticking pinyin like di4shang4 instead of di4 shang4
            Input: astring containing a pinyin like "di4shang4"
            Output: a string containing a pinyin like "di4 shang4"
            """

            clean_pinyin = ""
            for n in range(len(pinyin)):
                clean_pinyin += pinyin[n]
                if pinyin[n].isdigit() and (n < len(pinyin)-1):
                    if pinyin[n+1] != " ":
                        clean_pinyin += " "
            return clean_pinyin
        # end of unStick

        dictionary = dictname
        # Open the dictionary in text mode, read only
        with open(dictionary, mode="r") as dic:
            liste = dic.readlines()  # Use the text file as lines
        space_ind = []
        pinyin_delimiters = []
        translation_delimiters = []
        simplified_list = []
        traditional_list = []
        pinyin_list = []
        translation_list = []

        # Check if producted files already exist
        # Delete them if needed
        for fileName in ["simplified", "traditional", "translation", "pinyin"]:
            try:
                open(fileName, "r")
            except:
                pass
            else:
                shutil.move(fileName, fileName + "_saved")
                print("Warning: " + fileName + " has been moved to "
                      + fileName + "_saved.\n"
                      + "Indeed, this file will be created by Zhudi.")

        for i in liste:  # for each line
            space_ind = []
            pinyin_delimiters = []
            translation_delimiters = []
            translation = []

            if i[0] != "#":
                for k in range(len(i)):
                    if i[k] == " ":  # look for spaces
                        space_ind.append(k)
                    if i[k] == "[":  # look for pinyin delimiters
                        pinyin_delimiters.append(k)
                    if i[k] == "]":
                        pinyin_delimiters.append(k)
                    if i[k] == "/":  # look for translation delimiters
                        translation_delimiters.append(k)
                traditional = i[0:space_ind[0]]
                simplified = i[space_ind[0]+1:space_ind[1]]
                pinyin = i[pinyin_delimiters[0]+1:pinyin_delimiters[1]]
                for n in range(len(translation_delimiters) - 1):
                    translation.append(i[translation_delimiters[n] + 1:translation_delimiters[n + 1]])

                clean_pinyin = unStick(pinyin)
                translation_clean = ""
                for i in range(len(translation)):
                    if i != 0:
                        translation_clean += "/"
                    translation_clean += translation[i]

                pinyin_list.append(clean_pinyin)
                traditional_list.append(traditional)
                simplified_list.append(simplified)
                translation_list.append(translation_clean)

                with open("simplified", mode="a") as simplified_file:
                    simplified_file.write(simplified+"\n")
                with open("traditional", mode="a") as traditional_file:
                    traditional_file.write(traditional+"\n")
                with open("translation", mode="a") as translation_file:
                    translation_file.write(translation_clean+"\n")
                with open("pinyin", mode="a") as pinyin_file:
                    pinyin_file.write(clean_pinyin+"\n")

        return (simplified_list, traditional_list, translation_list, pinyin_list)
    # End of split()

    def read_files(self,
                   pinyin_file_name,
                   zhuyin_file_name,
                   traditional_file_name,
                   simplified_file_name,
                   translation_file_name):
        """ Reads some files needed to build the Dictionary class.
        Returns 5 lists:
        (pinyin, zhuyin, traditional, simplified, translation)
        """

        try:
            pinyin_file = open(pinyin_file_name, "r")
            pinyin = pinyin_file.readlines()
            pinyin_file.closed
            zhuyin_file = open(zhuyin_file_name, "r")
            zhuyin = zhuyin_file.readlines()
            zhuyin_file.closed
            traditional_file = open(traditional_file_name, "r")
            traditional = traditional_file.readlines()
            traditional_file.closed
            simplified_file = open(simplified_file_name, "r")
            simplified = simplified_file.readlines()
            simplified_file.closed
            translation_file = open(translation_file_name, "r")
            translation = translation_file.readlines()
            translation_file.closed
            return pinyin, zhuyin, traditional, simplified, translation
        except IOError:
            print("### The dictionary files couldn't be read. Make sure you have"
                  " split the dictonary file first. ###")
            quit()
        # End of read_files()

    def get_config(self):
        """ Reads the config file, if it exists, and returns a list of variables
        related to that file (of the form [var, value]).

        """
        try:
            open(os.environ["HOME"] + "/.zhudi/config", "r")
        except IOError:
            # If no config file found
            print("No config file found. Use defaults")
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


class SegmentationTools(object):
    """ This class is intended to contains any functions dealing with Chinese.
    In other words, any functions treating a sentence, a word, etc.
    """

    def __init__(self):
        """ Sets are aimed at speed performance.
        """

        self.trad_set = []
        self.simp_set = []
        self.set_of_chinese_chars = []

    def load(self, dataObject):
        """ Load and prepare needed data.
        """

        for style in [dataObject.traditional, dataObject.simplified]:
            temp = [[], [], [], [], [], [], [], [], [], [],
                    [], [], [], [], [], [], [], [], [], []]  # 20
            out = []
            for item in style:
                # get rid of the \n
                item = item[:-1]
                if len(item) <= 20:
                    temp[len(item)-1].append(item)
            for nested_list in temp:
                # transform in set for performance issue
                out.append(set(nested_list))
                if style == dataObject.traditional:
                    self.trad_set = out
                else:
                    self.simp_set = out
        dataObject.create_set_chinese_characters()
        self.set_of_chinese_chars = dataObject.set_of_chinese_chars
    # end of load()

    def isNotChinese(self, string):
        """
        Returns True is the given string does not contain any Chinese Character

        """
        for car in string:
            if ord(car) in self.set_of_chinese_chars:
                return False
        return True

    def searchUnique(self, word, dataObject):
        """ Search for a word in the dictionary.
        Returns only 1 result (the index) or None if nothing found.

        """
        def findIt(word, givenList):
            """ Returns the index of the found word.
            """

            cnt = 0
            for case in givenList:
                if case[-1] == "\n":
                    case = case[:-1]
                if word == case:
                    return cnt
                cnt += 1
            return None

        if self.isNotChinese(word):
            return None
        else:
            r1 = findIt(word, dataObject.traditional)
            r2 = findIt(word, dataObject.simplified)
            if r2 is None:
                if r1 is None:
                    return None
                return r1
            return r2

    def sentence_segmentation(self, string):
        """ Parse the string input for Chinese words based on words in our
        dictionary. Retuns a list of words.
        """

        def longest_word(string):
            traditional = self.trad_set
            simplified = self.simp_set
            maxi = 20
            if len(string) < maxi:
                upper = len(string)
            else:
                upper = maxi
            for i in range(upper, 1, -1):  # from max-1 to 1
                current_string = string[0:i]
                if self.isNotChinese(current_string):
                    return current_string
                if current_string in traditional[i-1]:
                    return current_string
                elif current_string in simplified[i-1]:
                    return current_string
        # end of longest_word

        output = []
        while len(string) >= 1:
            lw = longest_word(string)
            if lw is None:
                lw = string[0]
                string = string[1:]  # the character is alone
            else:
                string = string[len(lw):]
            if lw != " ":
                output.append(lw)
        return output
# end of ChineseProcessing


class DictionaryTools(object):
    """ Contains all functions needed for the dictionary part.
    """

    def __init__(self):
        self.index = []
        self.set_of_chinese_chars = []

    def pinyin_to_zhuyin(self, pinyin, dataObject):
        """Converts the given pinyin list into zhuyin. Returns a list."""
        pinyin_zhuyin_dict = dataObject.pinyin_to_zhuyin

        # for speed issue, transforme the list of pinyin in one long string
        to_convert = " " + " # ".join(pinyin)
        to_convert += " "  # This space is useful for the regexp matching
        to_convert = to_convert.lower()
        zhuyin = re.sub("u:", "ü", to_convert)  # change u: into ü
        zhuyin = re.sub(" r ", " er ", zhuyin)  # change r into er
        for i in range(len(pinyin_zhuyin_dict)):
            if i < len(pinyin_zhuyin_dict) - 5:
                zhuyin = re.sub(" " + pinyin_zhuyin_dict[i][0],
                                " " + pinyin_zhuyin_dict[i][1],
                                zhuyin)  # do not change the tones
            elif i >= len(pinyin_zhuyin_dict) - 5:
                zhuyin = re.sub(pinyin_zhuyin_dict[i][0] + " ",
                                pinyin_zhuyin_dict[i][1] + " ",
                                zhuyin)  # tones
        # delete the last space used for matching convenience
        zhuyin = zhuyin[:-1]
        # Break the long string as a list
        zhuyin = zhuyin.split(" # ")
        zhuyin[0] = zhuyin[0][1:]  # get rid of the first space
        return zhuyin

    def is_pinyin(self, pin1yin1):
        return re.match(r'^(?i)[a-z]+[0-5]', pin1yin1)

    def unicode_pinyin(self, pin1yin1):
        """ Convert a string representing a pinyin syllable with tone.
        Returns a string.

        Argument:
        A string like "ni3".
        """

        if not self.is_pinyin(pin1yin1):
            return pin1yin1

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
                    if vowels_list[i] == "i" and vowels_list[i + 1] == "u":
                        return True
                    return False

        vowels = find_vowels(syl)
        if is_there_iu(vowels):
            syl = syl.replace("u", tones[tone - 1][4])
            return syl
        # To check, in order: 'a','o','e','i','u','ü' (cf. Wikipedia)
        to_test = "aoeiuü"
        for case in to_test:
            if case in vowels:
                syl = syl.replace(case, tones[tone - 1][fifth_tone.find(case)])
                return syl

    def search(self, given_list, text):
        """ Search for a string in a list.

        Arguments:
        given_list: a list of words
        text: a string

        Searchs for "string" in "given_list". Returns a list of indices in the
        index attribute of the DictionaryTools class.

        """
        words = (text.lower()).split()
        index = []
        total = []
        # try in each line of the dic
        for k in range(len(given_list)):
            counter = 0
            for s in range(len(words)):
                # for each word of the request (case insensitive)
                if (given_list[k].lower()).count(words[s]) != 0:
                    counter += 1
                if counter == len(words):
                    # only accepts lines containing every words
                    index.append(k)
                    total.append(len(given_list[k]))
        d = dict(zip(index, total))
        dl = sorted(d.items(), key=lambda x: x[1])
        index = []
        # Keep the sorted results
        for i in range(len(dl)):
            index.append(dl[i][0])
        self.index = index
