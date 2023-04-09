import sqlite3
import json

from zhudi.data import Data
from zhudi.processing import DictionaryTools


def load_edict_dictionary(language: str, filename: str) -> None:
    print(f"Importing {filename} as {language} table...")
    # Remove commented license at the top of the file first

    # table needs: traditional, simplified, pinyin, zhuyin, definitions
    c = sqlite3.connect("zhudi-data/dictionaries.db")
    cursor = c.cursor()

    cursor.execute(f"""
    create table if not exists {language} (
        traditional text not null,
        simplified text not null,
        pinyin text not null,
        zhuyin text not null,
        definitions text not null
    ) strict;
    """)

    cursor.execute(f"delete from {language}")

    c.commit()

    query = f"insert into {language}(traditional, simplified, pinyin, zhuyin, definitions) values (?, ?, ?, ?, ?)"

    with open(f"zhudi-data/{filename}", 'r') as fd:
        lines = fd.readlines()
        data = []
        for line in lines:
            clean_line = line.replace('\n', '')
            parts = clean_line.split(' ')
            if (len(parts) < 4):
                print(f"Warning, ignored: {parts}")
            else:
                # Parse based on https://cc-cedict.org/wiki/format:syntax
                traditional = parts[0]
                simplified = parts[1]
                pinyin = clean_line.replace('[', '|').replace(']', '|').split('|')[1]
                # do not convert pinyin into unicode in db, but in app
                z = DictionaryTools.pinyin_to_zhuyin(pinyin.split(' '), Data())
                zhuyin = ' '.join(z)
                definitions = clean_line.split('/')[1:-1]
                data.append((traditional, simplified, pinyin, zhuyin, json.dumps(definitions)))
                if len(data) == 1000:
                    c.executemany(query, data)
                    data = []
        if len(data) != 0:
            c.executemany(query, data)
    c.commit()

def generate_full_text_search_table(language: str) -> None:
    print(f"Generating SQLite FTS5 (Full Text Search) for {language}...")
    c = sqlite3.connect("zhudi-data/dictionaries.db")
    cursor = c.cursor()

    cursor.execute(f"""
    create virtual table if not exists {language}_fts using fts5(
        traditional,
        simplified,
        pinyin,
        zhuyin,
        definitions,
        content={language}
    );
    """)
    cursor.execute(f"insert into  {language}_fts({language}_fts) values('delete-all');")

    cursor.execute(f"insert into {language}_fts (rowid, traditional, simplified, pinyin, zhuyin, definitions) select rowid, traditional, simplified, pinyin, zhuyin, definitions from {language};")

    cursor.execute(f"insert into {language}_fts({language}_fts) values('optimize');")

    c.commit()

if __name__ == '__main__':
    load_edict_dictionary('english', 'cedict_1_0_ts_utf-8_mdbg.txt')
    load_edict_dictionary('german', 'handedict.u8')
    load_edict_dictionary('french', 'cfdict.u8')

    generate_full_text_search_table('english')
    generate_full_text_search_table('german')
    generate_full_text_search_table('french')
