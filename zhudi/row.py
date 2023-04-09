from dataclasses import dataclass

from typing import List


@dataclass
class Row:
    traditional: str
    simplified: str
    pinyin: str
    zhuyin: str
    definitions: List[str]
