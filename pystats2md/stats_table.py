from __future__ import annotations
import math
import random
from typing import Optional, List
import copy

from pystats2md.helpers import *
from pystats2md.aggregation import Aggregation
from pystats2md.stats_plot import StatsPlot


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
        self.content = copy.deepcopy(content)
        self.header_row = copy.deepcopy(header_row)
        self.header_col = copy.deepcopy(header_col)

    def rows(self) -> int:
        return len(self.header_col)

    def cols(self) -> int:
        return len(self.header_row)

    def _column2index(self, column: str) -> int:
        if isinstance(column, int):
            return column
        assert isinstance(column, str), 'Must be a string'
        assert column in self.header_row, 'No such column'
        return index_of(self.header_row, column)

    def _numeric_value(self, row, col) -> float:
        v = self.content[row][col]
        if isinstance(v, (int, float)):
            return v
        elif isinstance(v, str):
            return float(v)
        else:
            return 0

    def _only_numerics(self, vals: list) -> list:
        return [v for v in vals if isinstance(v, (int, float))]

    def _only_col(self, col) -> List[float]:
        return [r[col] for r in self.content]

    def _only_row(self, row) -> List[float]:
        return self.content[row]

    def _column_title_and_values(self, col=None) -> (str, list):
        if col is None:
            vs = map(self._only_row, range(self.rows()))
            vs = map(self._only_numerics, vs)
            vs = map(Aggregation.take_mean, vs)
            return 'Mean', list(vs)
        else:
            col = self._column2index(col)
            return self.header_row[col], self._only_col(col)

    def normalize_values_in_column(self, column: int) -> StatsTable:
        col_idx = self._column2index(column)
        _, values = self._column_title_and_values(column)        
        biggest_val = max(values)

        for i, r in enumerate(self.content):
            r[col_idx] = values[i] / biggest_val            
        return self

    def normalize_values(self) -> StatsTable:
        for i in range(self.cols()):
            self.normalize_values_in_column(i)
        return self

    def add_gains(
        self,
        column=None,
        baseline_row=0,
    ) -> StatsTable:

        title, values = self._column_title_and_values(column)
        baseline = values[baseline_row]
        multipliers = [v / baseline for v in values]
        biggest = max(multipliers)
        for i, r in enumerate(self.content):
            gain = multipliers[i]
            if i == baseline_row:
                r.append(f'1x')
            elif gain == biggest:
                r.append('**' + num2str(gain) + 'x**')
            else:
                r.append(num2str(gain) + 'x')

        self.header_row.append(title + ' Gains')
        return self

    def add_ranking(
        self,
        column=None,
        bigger_is_better=True,
    ) -> StatsTable:

        title, values_per_row = self._column_title_and_values(column)
        values = sorted(values_per_row, reverse=bigger_is_better)
        for i, r in enumerate(self.content):
            idx = index_of(values, values_per_row[i])
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

        self.header_row.append(title + ' Ranking')
        return self

    def add_emoji(
        self,
        column=None,
        log_scale=False,
        bigger_is_better=True,
        impressive_gain=10,
    ) -> StatsTable:

        title, values_per_row = self._column_title_and_values(column)
        if len(values_per_row) <= 1:
            for r in self.content:
                r.append('')
            return self

        values = list(sorted(values_per_row))
        val_smallest = values[0]
        val_biggest = values[-1]
        second_biggest = values[-2]
        huge_leader_gap = (val_biggest / second_biggest) > impressive_gain
        diff = (val_biggest-val_smallest)
        biggest_bracket = val_biggest - diff/3
        smallest_bracket = val_smallest + diff/3

        if log_scale:
            log_small = math.log(val_smallest)
            log_big = math.log(val_biggest)
            diff = (log_big-log_small)
            biggest_bracket = math.exp(log_big - diff/3)
            smallest_bracket = math.exp(log_small - diff/3)

        for i, r in enumerate(self.content):
            val = values_per_row[i]
            if not isinstance(val, (int, float)):
                r.append('')
                continue

            is_average = smallest_bracket <= val <= biggest_bracket
            is_best = (val == val_biggest) if bigger_is_better else (
                val == val_smallest)
            is_good = (val >= biggest_bracket) if bigger_is_better else (
                val <= smallest_bracket)

            # This result has nothing special in it.
            if is_average:
                r.append('')
                continue

            # Pick any random emoji and repeat it 3 times (jackpot!).
            if is_best and huge_leader_gap:
                cool_empjis = [':fire:', ':strawberry:', ':underage:']
                icon = random.choice(cool_empjis)
                r.append(icon * 3)
                continue

            r.append(':thumbsup:' if is_good else ':thumbsdown:')

        # https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md
        # https://gist.github.com/AliMD/3344523
        self.header_row.append(title + ' Result')
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

    def printable_seconds(self) -> StatsTable:
        """
            Transforms the number in each cell from seconds 
            to more readable number of hours and minutes.
        """
        for row_idx, row in enumerate(self.content):
            for cell_idx, cell in enumerate(row):
                row[cell_idx] = secs2str(cell)
            self.content[row_idx] = row
        return self

    def printable_bytes(self) -> StatsTable:
        """
            Transforms the number in each cell from bytes 
            to more readable number of Gb, Mb & Kb...
        """
        for row_idx, row in enumerate(self.content):
            for cell_idx, cell in enumerate(row):
                row[cell_idx] = bytes2str(cell)
            self.content[row_idx] = row
        return self

    def plot(self, **kwargs) -> StatsPlot:
        return StatsPlot(table=self, **kwargs)
