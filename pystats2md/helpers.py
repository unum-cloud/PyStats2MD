from __future__ import annotations
from typing import List


def num2str(num: float) -> str:
    if num is None:
        return ''
    if isinstance(num, str):
        return num
    return '{:,.2f}'.format(num)


def str2num(str_: str) -> float:
    if str_ is None or len(str_) == 0:
        return None
    if isinstance(str_, float):
        return str_
    str_ = str_.replace(',', '')
    return float(str_)


def get_unique(dicts: list, key: str) -> Set[str]:
    return {num2str(s.get(key)) for s in dicts if key in s}


def index_of(vs: List[object], v: object) -> Optional[int]:
    try:
        return vs.index(v)
    except:
        return None


def table2str(table: List[List[str]]) -> str:
    lines = list()

    def render_line(cells: List[str]) -> str:
        line = ' | '.join(cells)
        line = f'| {line} |'
        return line

    for idx_row in range(len(table)):
        cells = table[idx_row]
        lines.append(render_line(cells))
        if idx_row == 0:
            delimeters = [':---'] + [':---:'] * (len(cells) - 1)
            lines.append(render_line(delimeters))
    return '\n'.join(lines)
