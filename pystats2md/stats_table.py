from __future__ import annotations
import math
import random
from typing import Optional, List

from pystats2md.helpers import *


class StatsTable(object):

    def __init__(
        self,
        content: List[List[str]],
        header_row: Optional[List[str]],
        header_col: Optional[List[str]],
    ):
        assert isinstance(content, list)
        if header_row is not None:
            assert isinstance(header_row, list)
        if header_col is not None:
            assert isinstance(header_col, list)
        self.content = content
        self.header_row = header_row
        self.header_col = header_col

    def _column2index(self, column: str) -> int:
        if isinstance(column, int):
            return column
        assert isinstance(column, str), 'Must be a string'
        assert column in self.header_row, 'No such column'
        return index_of(self.header_row, column)

    def add_gains(
        self,
        column=-1,
        baseline_row=0,
    ) -> StatsTable:

        column = self._column2index(column)
        self.header_row.append(f'Gains in {self.header_row[column]}')

        baseline = self.content[baseline_row][column]
        for i, r in enumerate(self.content):
            if i == baseline_row:
                r.append(f'1x')
            else:
                gain = float(r[column]) / baseline
                r.append(num2str(gain) + 'x')
        return self

    def add_ranking(
        self,
        column=-1,
        bigger_is_better=True,
    ) -> StatsTable:

        column = self._column2index(column)
        self.header_row.append(f'Ranking by {self.header_row[column]}')

        values = [r[column] for r in self.content]
        values = [v for v in values if isinstance(v, (int, float))]
        values = sorted(values, reverse=bigger_is_better)
        for r in self.content:
            idx = index_of(values, r[column])
            if idx is None:
                r.append('')
            else:
                if idx == 0:
                    r.append(':1st_place_medal:')
                elif idx == 1:
                    r.append(':2nd_place_medal:')
                elif idx == 2:
                    r.append(':3rd_place_medal:')
                else:
                    r.append(f'# {idx + 1}')
        return self

    def add_emoji(
        self,
        column=-1,
        log_scale=False,
        bigger_is_better=True,
    ) -> StatsTable:

        column = self._column2index(column)
        # https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md
        # https://gist.github.com/AliMD/3344523
        self.header_row.append(f'Good in {self.header_row[column]}')

        values = [r[column] for r in self.content]
        values = [v for v in values if isinstance(v, (int, float))]
        if len(values) <= 1:
            for r in self.content:
                r.append('')
            return self

        values = sorted(values)
        val_smallest = values[0]
        val_biggest = values[-1]
        second_biggest = values[-2]
        huge_leader_gap = (val_biggest / second_biggest) > 10
        diff = (val_biggest-val_smallest)
        biggest_bracket = val_biggest - diff/3
        worst_bracket = val_smallest + diff/3

        if log_scale:
            log_small = math.log(val_smallest)
            log_big = math.log(val_biggest)
            diff = (log_big-log_small)
            biggest_bracket = math.exp(log_big - diff/3)
            worst_bracket = math.exp(log_small - diff/3)

        for r in self.content:
            val = r[column]
            if not isinstance(val, (int, float)):
                r.append('')
                continue
            # This result has nothing special in it.
            if worst_bracket <= val <= biggest_bracket:
                r.append('')
                continue

            # Pick any random emoji and repeat it 3 times (jackpot!).
            is_best = (val == val_biggest) if bigger_is_better else (
                val == val_smallest)
            if is_best and huge_leader_gap:
                cool_empjis = [':fire:', ':strawberry:', ':underage:']
                icon = random.choice(cool_empjis)
                r.append(icon * 3)

            #
            is_good = (val >= biggest_bracket) if bigger_is_better else (
                val <= worst_bracket)
            if is_good:
                r.append(':thumbsup:')
            else:
                r.append(':thumbsdown:')

        return self

    def print(self) -> str:
        assert len(self.content) > 0, 'Empty table!'
        assert len(self.header_col) == len(
            self.content), 'Mismatch in rows number'
        assert len(self.header_row) == len(
            self.content[0]), 'Mismatch in cols number'

        result = list()
        result.append(list())
        result[0].append('')
        result[0].extend(self.header_row)
        content_strs = [[num2str(c) for c in r] for r in self.content]

        for idx_row in range(len(self.header_col)):
            result.append(list())
            result[idx_row+1].append(self.header_col[idx_row])
            result[idx_row+1].extend(content_strs[idx_row])

        return table2str(result)
