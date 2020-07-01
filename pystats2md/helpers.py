from __future__ import annotations
from typing import List, Optional, Set
from random import choice
from string import ascii_lowercase


def secs2str(num: float) -> str:
    if not isinstance(num, float):
        if isinstance(num, int):
            num = float(num)
        elif isinstance(num, str):
            num = float(num)
        else:
            return ''

    hours = num // 3600
    mins = (num % 3600) // 60
    secs = (num % 3600) % 60
    if hours > 0:
        return '{:,.0f} hours, {:,.0f} mins'.format(hours, mins)
    else:
        return '{:,.0f} mins, {:,.0f} secs'.format(mins, secs)


def bytes2str(num: int) -> str:
    if not isinstance(num, int):
        if isinstance(num, float):
            num = int(num)
        elif isinstance(num, str):
            num = int(num)
        else:
            return ''

    power = 2**10  # 2**10 = 1024
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while num > power:
        num /= power
        n += 1
    return f'{num} {power_labels[n]}b'


def metric2str(num: float, decimal_places=1) -> str:
    if not isinstance(num, float):
        if isinstance(num, int):
            num = float(num)
        elif isinstance(num, str):
            num = float(num)
        else:
            return ''

    for unit in ['', 'K', 'M', 'G', 'T']:
        if num < 1000.0:
            break
        num /= 1000.0
    return f'{num:.{decimal_places}f} {unit}'


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

def random_str(letters: int = 8) -> str:
    return ''.join(choice(ascii_lowercase) for i in range(letters))