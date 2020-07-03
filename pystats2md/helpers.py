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


def metric2str(
    num: float, decimal_places=1,
    units=['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'],
    step=1000.0
) -> str:
    if not isinstance(num, float):
        if isinstance(num, int):
            num = float(num)
        elif isinstance(num, str):
            num = float(num)
        else:
            return ''

    for unit in units:
        if num < step:
            break
        num /= step
    return f'{num:,.{decimal_places}f} {unit}'


def bytes2str(num: int, decimal_places=1) -> str:
    return metric2str(
        num=num,
        decimal_places=decimal_places,
        units=['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
        step=1024
    )


def bits2str(num: int, decimal_places=1) -> str:
    return metric2str(
        num=num,
        decimal_places=decimal_places,
        units=['bits', 'Kib', 'Mib', 'Gib', 'Tib', 'Pib', 'Eib', 'Zib', 'Yib'],
        step=1024
    )


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
