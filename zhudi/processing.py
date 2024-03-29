# coding: utf-8

import re
import shutil

from zhudi.data import Data
from zhudi.preferences import Preferences


class PreProcessing(object):
    """This class is in charge of the pre-processing needed to launch Zhudi.
    It loads config files, split dictionaries, etc.
    """

    def __init__(self):
        pass

    @staticmethod
    def split(dictname):
        """Loads the *.u8 file and split it. Return a tuple of 4 lists:
        (simplified_list,
        traditional_list,
        translation_list,
        pinyin_list)
        """

        def unstick(pinyin):
            """Get rid of sticking pinyin like di4shang4 instead of di4 shang4
            Input: a string containing a pinyin like "di4shang4"
            Output: a string containing a pinyin like "di4 shang4"
            """

            clean_pinyin = ""
            for index in range(len(pinyin)):
                clean_pinyin += pinyin[index]
                if pinyin[index].isdigit() and (index < len(pinyin) - 1):
                    if pinyin[index + 1] != " ":
                        clean_pinyin += " "
            return clean_pinyin

        # end of unstick

        dictionary = dictname
        # Open the dictionary in text mode, read only
        with open(dictionary, mode="r") as dic:
            liste = dic.readlines()  # Use the text file as lines
        simplified_list = []
        traditional_list = []
        pinyin_list = []
        translation_list = []

        # Check if produced files already exist
        # Delete them if needed
        for filename in ["simplified", "traditional", "translation", "pinyin"]:
            try:
                open(filename, "r")
            except:
                pass
            else:
                shutil.move(filename, filename + "_saved")
                print(
                    "Warning: "
                    + filename
                    + " has been moved to "
                    + filename
                    + "_saved.\n"
                    + "Indeed, this file will be created by Zhudi."
                )

        for i in liste:  # for each line
            space_ind = []
            pinyin_delimiters = []
            translation_delimiters = []
            translation = []
            try:
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
                    traditional = i[0 : space_ind[0]]
                    simplified = i[space_ind[0] + 1 : space_ind[1]]
                    pinyin = i[pinyin_delimiters[0] + 1 : pinyin_delimiters[1]]
                    for index in range(len(translation_delimiters) - 1):
                        translation.append(
                            i[
                                translation_delimiters[index]
                                + 1 : translation_delimiters[index + 1]
                            ]
                        )

                    clean_pinyin = unstick(pinyin)
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
                        simplified_file.write(simplified + "\n")
                    with open("traditional", mode="a") as traditional_file:
                        traditional_file.write(traditional + "\n")
                    with open("translation", mode="a") as translation_file:
                        translation_file.write(translation_clean + "\n")
                    with open("pinyin", mode="a") as pinyin_file:
                        pinyin_file.write(clean_pinyin + "\n")
            except IndexError:
                print("Warning: Could not parse the following line:")
                print("\t'" + i + "'")
            except Exception as error:
                print(
                    "Error: An unknown error occurred while parsing the following line:"
                )
                print("\t'" + i + "'")
                print(str(error))

        return simplified_list, traditional_list, translation_list, pinyin_list

    # End of split()

    @staticmethod
    def read_files(
        pinyin_file_name,
        zhuyin_file_name,
        traditional_file_name,
        simplified_file_name,
        translation_file_name,
    ):
        """Reads some files needed to build the Dictionary class.
        Returns 5 lists:
        (pinyin, zhuyin, traditional, simplified, translation)
        """

        try:
            pinyin_file = open(pinyin_file_name, "r")
            pinyin = [
                (
                    lambda p: p
                    + "/"
                    + p.replace(" ", "")
                    + "/"
                    + re.sub(r"[ \d]", "", p)
                )(p.replace("u:", "v"))
                for p in pinyin_file.readlines()
            ]
            pinyin_file.close()
            zhuyin_file = open(zhuyin_file_name, "r")
            zhuyin = zhuyin_file.readlines()
            zhuyin_file.close()
            traditional_file = open(traditional_file_name, "r")
            traditional = traditional_file.readlines()
            traditional_file.close()
            simplified_file = open(simplified_file_name, "r")
            simplified = simplified_file.readlines()
            simplified_file.close()
            translation_file = open(translation_file_name, "r")
            translation = translation_file.readlines()
            translation_file.close()
            return pinyin, zhuyin, traditional, simplified, translation
        except IOError:
            print(
                "### The dictionary files couldn't be read. Make sure you have"
                " split the dictionary file first. ###"
            )
            quit()
        # End of read_files()


class SegmentationTools(object):
    """This class is intended to contain any functions dealing with Chinese.
    In other words, any functions treating a sentence, a word, etc.
    """

    def __init__(self):
        """Sets are aimed at speed performance."""

        self.trad_set = []
        self.simp_set = []
        self.set_of_chinese_chars = []

    def load(self, data_obj):
        """Load and prepare needed data."""

        for style in [data_obj.traditional, data_obj.simplified]:
            temp = [
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            ]  # 20
            out = []
            for item in style:
                # get rid of the \n
                item = item[:-1]
                if len(item) <= 20:
                    temp[len(item) - 1].append(item)
            for nested_list in temp:
                # transform in set for performance issue
                out.append(set(nested_list))
                if style == data_obj.traditional:
                    self.trad_set = out
                else:
                    self.simp_set = out
        data_obj.create_set_chinese_characters()
        self.set_of_chinese_chars = data_obj.set_of_chinese_chars

    # end of load()

    def is_not_chinese(self, string):
        """
        Returns True is the given string does not contain any Chinese Character

        """
        for car in string:
            if ord(car) in self.set_of_chinese_chars:
                return False
        return True

    def search_unique(self, word, data_obj):
        """Search for a word in the dictionary.
        Returns only 1 result (the index) or None if nothing found.

        """

        def find_it(word, given_list):
            """Returns the index of the found word."""

            cnt = 0
            for case in given_list:
                if case[-1] == "\n":
                    case = case[:-1]
                if word == case:
                    return cnt
                cnt += 1
            return None

        if self.is_not_chinese(word):
            return None
        else:
            r1 = find_it(word, data_obj.traditional)
            r2 = find_it(word, data_obj.simplified)
            if r2 is None:
                if r1 is None:
                    return None
                return r1
            return r2

    def sentence_segmentation(self, string):
        """Parse the string input for Chinese words based on words in our
        dictionary. Retuns a list of words.
        """

        def longest_word(string):
            """
            Returns the longest word from a given string.

            """
            traditional = self.trad_set
            simplified = self.simp_set
            maxi = 20
            if len(string) < maxi:
                upper = len(string)
            else:
                upper = maxi
            for i in range(upper, 1, -1):  # from max-1 to 1
                current_string = string[0:i]
                if self.is_not_chinese(current_string):
                    return current_string
                if current_string in traditional[i - 1]:
                    return current_string
                elif current_string in simplified[i - 1]:
                    return current_string

        # end of longest_word

        output = []
        while len(string) >= 1:
            long_word = longest_word(string)
            if long_word is None:
                long_word = string[0]
                string = string[1:]  # the character is alone
            else:
                string = string[len(long_word) :]
            if long_word != " ":
                output.append(long_word)
        return output


# end of ChineseProcessing


class DictionaryTools(object):
    """Contains all functions needed for the dictionary part."""

    def __init__(self):
        self.index = []
        self.set_of_chinese_chars = []

    @staticmethod
    def pinyin_to_zhuyin(pinyin, data_obj):
        """Converts the given pinyin list into zhuyin. Returns a list."""
        pinyin_zhuyin_dict = data_obj.pinyin_to_zhuyin

        # for speed issue, transform the list of pinyin in one long string
        to_convert = " " + " # ".join(pinyin)
        to_convert += " "  # This space is useful for the regexp matching
        to_convert = to_convert.lower()
        zhuyin = re.sub("u:", "ü", to_convert)  # change u: into ü
        zhuyin = re.sub("v", "ü", zhuyin)  # change v into ü
        zhuyin = re.sub(" r ", " er ", zhuyin)  # change r into er
        for i in range(len(pinyin_zhuyin_dict)):
            if i < len(pinyin_zhuyin_dict) - 5:
                zhuyin = re.sub(
                    " " + pinyin_zhuyin_dict[i][0],
                    " " + pinyin_zhuyin_dict[i][1],
                    zhuyin,
                )  # do not change the tones
            elif i >= len(pinyin_zhuyin_dict) - 5:
                zhuyin = re.sub(
                    pinyin_zhuyin_dict[i][0] + " ",
                    pinyin_zhuyin_dict[i][1] + " ",
                    zhuyin,
                )  # tones
        # delete the last space used for matching convenience
        zhuyin = zhuyin[:-1]
        # Break the long string as a list
        zhuyin = zhuyin.split(" # ")
        zhuyin[0] = zhuyin[0][1:]  # get rid of the first space
        return zhuyin

    @staticmethod
    def is_pinyin(pin1yin1):
        """
        Returns True if the input looks like a pinyin string. False otherwise.

        """
        return re.match(r"(?i)^[a-züÜ]+[0-5]", pin1yin1)

    @staticmethod
    def unicode_pinyin(pin1yin1):
        """Convert a string representing a pinyin syllable with tone.
        Returns a string.

        Argument:
        A string like "ni3".
        """

        pin1yin1 = re.sub("u:", "ü", pin1yin1)
        pin1yin1 = re.sub("v", "ü", pin1yin1)
        pin1yin1 = re.sub("U:", "Ü", pin1yin1)
        pin1yin1 = re.sub("V", "Ü", pin1yin1)
        if not DictionaryTools.is_pinyin(pin1yin1):
            return pin1yin1

        syl = pin1yin1[:-1]
        tone = int(pin1yin1[-1])
        first_tone = "āĀēĒīĪōŌūŪǖǕ"
        second_tone = "áÁéÉíÍóÓúÚǘǗ"
        third_tone = "ǎǍěĚǐǏǒǑǔǓǚǙ"
        fourth_tone = "àÀèÈìÌòÒùÙǜǛ"
        fifth_tone = "aAeEiIoOuUüÜ"
        tones = [first_tone, second_tone, third_tone, fourth_tone, fifth_tone]

        if "iu" in syl:
            return syl.replace("u", tones[tone - 1][-4])

        # To check, in order: 'a','o','e','i','u','ü' (cf. Wikipedia)
        to_test = "aAoOeEiIuUüÜ"
        for i, case in enumerate(to_test):
            if case in syl:
                return syl.replace(case, tones[tone - 1][fifth_tone.find(case)])

        return pin1yin1

    @staticmethod
    def romanize(data_object: Data, index: int, preferences: Preferences):
        if preferences.get_romanization() == "zhuyin":
            zhuyins = data_object.zhuyin[index].split()
            # Add [] arround the pronunciation parts
            return "".join(f"[{zy}]" for zy in zhuyins)
        else:
            pinyins = data_object.pinyin[index].split("/", 1)[0].split()
            return " ".join(DictionaryTools.unicode_pinyin(py) for py in pinyins)

    @staticmethod
    def romanize_pinyin(pinyin):
        try:
            return " ".join(DictionaryTools.unicode_pinyin(py) for py in pinyin.split())
        except:
            return pinyin

    def reset_search(self):
        self.index = []

    def finish_search(self, data_object):
        self.index = sorted(
            set(self.index),
            key=lambda x: (len(data_object.traditional[x]), data_object.traditional[x]),
        )[:500]

    def search(self, given_list, text):
        """Search for a string in a list.

        Arguments:
        given_list: a list of words
        text: a string

        Searches for "string" in "given_list". saves a list of indices in the
        index attribute of the DictionaryTools class.

        """
        words = (text.lower()).split()
        index = []
        # try in each line of the dic
        for line in range(len(given_list)):
            to_search = given_list[line].lower()
            # for each word of the request (case-insensitive)
            # only accepts lines containing every words
            if all(word in to_search for word in words):
                index.append(line)
        self.index.extend(index)
