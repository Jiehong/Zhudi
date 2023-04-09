from pathlib import PurePath
import json
import os
import sqlite3
from typing import List

from zhudi.row import Row


class Dictionaries:
    def __init__(self):
        self.connection = Dictionaries._load_config()
        self.set_of_chinese_chars = set()

    @staticmethod
    def _load_config() -> sqlite3.Connection:
        p = PurePath(os.path.realpath(__file__)).parent.parent.joinpath(
            "zhudi-data", "dictionaries.db"
        )
        return sqlite3.connect(p)

    def create_set_chinese_characters(self):
        """
        Create the set of all Chinese characters
        """

        chinese_characters = []
        # Han # So [26] CJK RADICAL REPEAT, CJK RADICAL RAP
        chinese_characters += [x for x in range(0x2E80, 0x2E9A)]
        # Han # So [89] CJK RADICAL CHOKE, CJK RADICAL C-SIMPLIFIED TURTLE
        chinese_characters += [x for x in range(0x2E9B, 0x2EF4)]
        # Han # So [214] KANGXI RADICAL ONE, KANGXI RADICAL FLUTE
        chinese_characters += [x for x in range(0x2F00, 0x2FD6)]
        # Han # Lm IDEOGRAPHIC ITERATION MARK
        chinese_characters.append(0x3005)
        # Han # Nl IDEOGRAPHIC NUMBER ZERO
        chinese_characters.append(0x3007)
        # Han # Nl [9] HANGZHOU NUMERAL ONE, HANGZHOU NUMERAL NINE
        chinese_characters += [x for x in range(0x3021, 0x302A)]
        # Han # Nl [3] HANGZHOU NUMERAL TEN, HANGZHOU NUMERAL THIRTY
        chinese_characters += [x for x in range(0x3038, 0x303B)]
        # Han # Lm VERTICAL IDEOGRAPHIC ITERATION MARK
        chinese_characters.append(0x303B)
        # Han # Lo [6582] CJK UNIFIED IDEOGRAPH-3400, CJK UNIFIED IDEOGRAPH-4DB5
        chinese_characters += [x for x in range(0x3400, 0x4DB6)]
        # Han # Lo [20932] CJK UNIFIED IDEOGRAPH-4E00, CJK UNIFIED IDEOGRAPH-9FC3
        chinese_characters += [x for x in range(0x4E00, 0x9FC4)]
        # Han # Lo [302] CJK COMPATIBILITY IDEOGRAPH-F900, CJK COMPATIBILITY IDEOGRAPH-FA2D
        chinese_characters += [x for x in range(0xF900, 0xFA2E)]
        # Han # Lo [59] CJK COMPATIBILITY IDEOGRAPH-FA30, CJK COMPATIBILITY IDEOGRAPH-FA6A
        chinese_characters += [x for x in range(0xFA30, 0xFA6B)]
        # Han # Lo [106] CJK COMPATIBILITY IDEOGRAPH-FA70, CJK COMPATIBILITY IDEOGRAPH-FAD9
        chinese_characters += [x for x in range(0xFA70, 0xFADA)]
        # Han # Lo [42711] CJK UNIFIED IDEOGRAPH-20000, CJK UNIFIED IDEOGRAPH-2A6D6
        chinese_characters += [x for x in range(0x20000, 0x2A6D7)]
        # Han # Lo [542] CJK COMPATIBILITY IDEOGRAPH-2F800, CJK COMPATIBILITY IDEOGRAPH-2FA1D
        chinese_characters += [x for x in range(0x2F800, 0x2FA1E)]

        self.set_of_chinese_chars = set(chinese_characters)

    def search(self, query: str, limit: int = 100) -> List[Row]:
        sql_query = f"""
        select traditional, simplified, pinyin, zhuyin, definitions
        from english_fts('{query}')
        order by rank
        limit {limit};"""

        rows = self.connection.cursor().execute(sql_query).fetchall()
        if rows is None or len(rows) == 0:
            return []

        output = []
        for row in rows:
            definitions = json.loads(row[-1])
            output.append(Row(row[0], row[1], row[2], row[3], definitions))
        return output

    def get_languages(self) -> List[str]:
        cursor = self.connection.cursor()
        query = """
            select name
            from sqlite_schema
            where
                type='table' and
                name not like '%_fts%'
            """
        values = cursor.execute(query).fetchall()
        return [x[0] for x in values]
