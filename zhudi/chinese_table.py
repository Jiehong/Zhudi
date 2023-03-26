# coding: utf-8
import sqlite3

from typing import List


class ChineseTable(object):
    """Abstract class aimed at providing common methods for each tables."""

    def __init__(self):
        self.keys_faces = ""
        self.keys_displayed_faces = []
        self.dictionary = ""

    def proceed(self, character: str) -> List[str]:
        """Returns the key code of the character as a code and as displayed_faces."""
        c = sqlite3.connect("zhudi-data/input_methods.db")
        cursor = c.cursor()
        query = f"""
        select code
        from {self.dictionary}
        where characters='{character}'
        order by code desc
        limit 1
        """
        codes = cursor.execute(query).fetchall()

        output = []
        for code in codes:
            displayed_code = ""
            for letter in code[0]:
                letter_pos = self.keys_faces.rfind(letter)
                displayed_code += self.keys_displayed_faces[letter_pos]
            output.append(code[0])
            output.append(displayed_code)
        return output


class Cangjie5Table(ChineseTable):
    """Contains the full cangjie5 input method information."""

    def __init__(self):
        super(Cangjie5Table, self).__init__()
        # Set the keys and keys_faces
        self.keys_faces = "abcdefghijklmnopqrstuvwxyz".upper()
        self.keys_displayed_faces = "日月金木水火土竹戈十大中一弓人心手口尸廿山女田難卜重"
        self.dictionary = "cangjie5"


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
        self.dictionary = "array30"


class Wubi86Table(ChineseTable):
    """Contains the full Wubi86 input table information."""

    def __init__(self):
        super(Wubi86Table, self).__init__()
        # Set the keys and keys_faces
        self.keys_faces = "abcdefghijklmnopqrstuvwxyz".upper()
        self.keys_displayed_faces = "abcdefghijklmnopqrstuvwxyz".upper()
        self.dictionary = "wubi86"
