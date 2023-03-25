# coding: utf-8

import collections
from typing import List


class ChineseTable(object):
    """Abstract class aimed at providing common methods for each tables."""

    def __init__(self):
        self.keys_faces = ""
        self.keys_displayed_faces = []

    def proceed(self, character: str, dictionary) -> List[str]:
        """Returns the key code of the character as a code and as displayed_faces."""
        output = []
        if character not in dictionary:
            code = character
            displayed_code = character
        else:
            code = dictionary[character]
            displayed_code = ""
            for letter in code:
                letter_pos = self.keys_faces.rfind(letter)
                displayed_code += self.keys_displayed_faces[letter_pos]
        output.append(code)
        output.append(displayed_code)
        return output

    @staticmethod
    def load(file_name):
        """Read codes from a file, and return a dictionary of codes
        and a dictionary of short codes

        """
        output = collections.defaultdict()
        output_short = collections.defaultdict()
        with open(file_name, "r") as a_file:
            lines = a_file.readlines()
            for line in lines:
                space_pos = line.rfind(" ")
                keys = line[0:space_pos]
                char = line[space_pos + 1 : -1]
                if char in output and len(keys) >= len(output[char]):
                    output_short[char] = output[char]
                    output[char] = keys
                elif char in output and len(keys) < len(output[char]):
                    output_short[char] = keys
                elif char not in output:
                    output[char] = keys
        return output, output_short


class Cangjie5Table(ChineseTable):
    """Contains the full cangjie5 input method information."""

    def __init__(self):
        super(Cangjie5Table, self).__init__()
        # Set the keys and keys_faces
        self.keys_faces = "abcdefghijklmnopqrstuvwxyz"
        self.keys_displayed_faces = "日月金木水火土竹戈十大中一弓人心手口尸廿" "山女田難卜重"


class Array30Table(ChineseTable):
    """Contains the full Array30 input method information."""

    def __init__(self):
        super(Array30Table, self).__init__()
        # Set the keys and keys_faces
        self.keys_faces = "qwertyuiopasdfghjkl;zxcvbnm,./"
        self.keys_displayed_faces = [
            "1↑",
            "2↑",
            "3↑",
            "4↑",
            "5↑",
            "6↑",
            "7↑",
            "8↑",
            "9↑",
            "0↑",
            "1-",
            "2-",
            "3-",
            "4-",
            "5-",
            "6-",
            "7-",
            "8-",
            "9-",
            "0-",
            "1↓",
            "2↓",
            "3↓",
            "4↓",
            "5↓",
            "6↓",
            "7↓",
            "8↓",
            "9↓",
            "0↓",
        ]


class Wubi86Table(ChineseTable):
    """Contains the full Wubi86 input table information."""

    def __init__(self):
        super(Wubi86Table, self).__init__()
        # Set the keys and keys_faces
        self.keys_faces = "abcdefghijklmnopqrstuvwxyz"
        self.keys_displayed_faces = "abcdefghijklmnopqrstuvwxyz".upper()
