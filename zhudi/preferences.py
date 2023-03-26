import os
import sqlite3
from sqlite3 import Connection


class Preferences:
    def __init__(self):
        self.connection = Preferences._load_config()

    @staticmethod
    def _load_config() -> Connection:
        try:
            path = os.environ["XDG_CONFIG_HOME"]
        except KeyError:
            path = None
        if path is None or path == "":
            path = os.environ["HOME"] + "/.config"

        path += "/zhudi"
        os.makedirs(path, exist_ok=True)

        c = sqlite3.connect(path + "/preferences.db")
        cursor = c.cursor()
        query = """
        create table if not exists preferences (
            key text primary key,
            value text not null
        )
        strict;
        """

        cursor.execute(query)

        c.commit()
        return c

    def get_romanization(self) -> str:
        cursor = self.connection.cursor()
        query = """
        select value
        from preferences
        where key='romanization'
        limit 1;
        """
        values = cursor.execute(query).fetchone()

        if values is None or values == []:
            default_value = "pinyin"
            self.set_romanization(default_value)
            return default_value
        return values[0]

    def set_romanization(self, value: str) -> None:
        cursor = self.connection.cursor()
        query = f"""
            insert into preferences (key, value)
            values ('romanization', '{value.lower()}')
            on conflict (key)
            do update set value = '{value.lower()}';
            """
        cursor.execute(query)
        self.connection.commit()

    def get_character_set(self) -> str:
        cursor = self.connection.cursor()
        query = """
        select value
        from preferences
        where key='character_set'
        limit 1;
        """
        values = cursor.execute(query).fetchone()

        if values is None or values == []:
            default_value = "simplified"
            self.set_character_set(default_value)
            return default_value
        return values[0]

    def set_character_set(self, value: str) -> None:
        cursor = self.connection.cursor()
        query = f"""
                insert into preferences (key, value)
                values ('character_set', '{value.lower()}')
                on conflict (key)
                do update set value = '{value.lower()}';
                """
        cursor.execute(query)
        self.connection.commit()
