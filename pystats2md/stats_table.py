import math
import random

from pystats2md.helpers import *


class StatsTable(object):

    def __init__(
        self,
        content: List[List[str]],
        header_row: Optional[List[str]],
        header_col: Optional[List[str]],
    ):
        self.content = content
        self.header_row = header_row
        self.header_col = header_col

    def _column2index(self, column: str) -> int:
        if isinstance(column, int):
            return column
        assert isinstance(column, str), 'Must be a string'
        assert column in self.header_row, 'No such column'
        return index_of(self.header_row, column)

    def add_gains(self, column=-1, baseline_row=0) -> StatsTable:
        column = self._column2index(column)
        self.header_row.append(f'Gains in {self.header_row[column]}')
        baseline = self.content[baseline_row][column]
        for i, r in enumerate(self.content):
            if i == baseline_row:
                r.append(f'1x')
            else:
                gain = float(r[column]) / baseline
                r.append(num2str(gain) + 'x')

    def add_ranking(self, column=-1) -> StatsTable:
        self.header_row.append(f'Ranking by {self.header_row[column]}')
        values = [r[column] for r in self.content]
        values = [v for v in values if isinstance(v, (int, float))]
        values = sorted(values)
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

    def add_emoji(self, column: int, log_scale=False) -> StatsTable:
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
        value_smallest = values[0]
        value_biggest = values[-1]
        second_biggest = values[-2]
        huge_leader_gap = (value_biggest / second_biggest) > 10
        diff = (value_biggest-value_smallest)
        best_bracket_smalest_val = value_biggest - diff/3
        worst_bracket_biggest_val = value_smallest + diff/3

        if log_scale:
            log_small = math.log(value_smallest)
            log_big = math.log(value_biggest)
            diff = (log_big-log_small)
            best_bracket_smalest_val = math.exp(log_big - diff/3)
            worst_bracket_biggest_val = math.exp(log_small - diff/3)

        for r in self.content:
            val = r[column]
            if not isinstance(val, (int, float)):
                r.append('')
            elif val >= best_bracket_smalest_val:
                if val == value_biggest and huge_leader_gap:
                    # Pick any random emoji and repeat it 3 times (jackpot!).
                    cool_empjis = [':fire:', ':strawberry:', ':underage:']
                    icon = random.choice(cool_empjis)
                    r.append(icon * 3)
                else:
                    r.append(':thumbsup:')
            elif val < worst_bracket_biggest_val:
                r.append(':thumbsdown:')
            else:
                r.append('')
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
