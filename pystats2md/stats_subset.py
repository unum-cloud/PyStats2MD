from __future__ import annotations
import copy
import re  # Filtering
import itertools  # Combinations of grouping keys

from pystats2md.helpers import *
from pystats2md.aggregation import Aggregation
import pystats2md.stats_file as sf
import pystats2md.stats_table as st


class StatsSubset(object):

    def __init__(self, source=None):
        self.dicts_list = list()
        self.include(source)

    def include(self, contents: List[dict]) -> StatsSubset:
        if contents is None:
            return self
        elif isinstance(contents, list):
            self.dicts_list.extend(copy.deepcopy(contents))
            return self
        elif isinstance(contents, sf.StatsFile):
            self.dicts_list.extend(contents.benchmarks.copy())
            return self
        elif isinstance(contents, str):
            return self.include(sf.StatsFile(contents))

    def filtered(self, **filters) -> StatsSubset:
        self.dicts_list = StatsSubset.filter(self.dicts_list, **filters)
        return self

    def compacted(self, **aggregation_policies) -> StatsSubset:
        self.dicts_list = StatsSubset.compact(
            self.dicts_list, **aggregation_policies)
        return self

    def grouped(self, *grouping_keys, **aggregation_policies) -> StatsSubset:
        self.dicts_list = StatsSubset.group(
            self.dicts_list, *grouping_keys, **aggregation_policies)
        return self

    def to_table(
        self,
        row_name_property: str,
        col_name_property: str,
        cell_content_property: str,
        row_names: List[str] = [],
        col_names: List[str] = [],
        include_headers=True,
    ) -> StatsTable:
        """
            Transforms the list of stats into a 2D table.
            Performs no type conversions and assumes the data
            is already `compact()`-ed to have just 1 entry per
            combination of (`row_name`, `col_name`).

            If no names are provided for rows and columns, 
            we will add all combinations.
        """

        if len(row_names) == 0:
            row_names = get_unique(self.dicts_list, row_name_property)
            row_names = sorted(list(row_names))
        if len(col_names) == 0:
            col_names = get_unique(self.dicts_list, col_name_property)
            col_names = sorted(list(col_names))

        result = list()
        for _ in row_names:
            result.append([None] * len(col_names))
        for s in self.dicts_list:
            if not ((row_name_property in s) and
                    (col_name_property in s) and
                    (cell_content_property in s)):
                continue
            idx_row = index_of(row_names, s.get(row_name_property, None))
            idx_col = index_of(col_names, s.get(col_name_property, None))
            if (idx_row is None) or (idx_col is None):
                continue
            result[idx_row][idx_col] = s.get(cell_content_property, None)

        return st.StatsTable(content=result, header_row=col_names, header_col=row_names)

    @staticmethod
    def predicate(**filters) -> object:
        def matches(s):
            for property_name, filter_criterea in filters.items():
                assert isinstance(
                    property_name, str), 'Undefined key in the filter'
                assert (filter_criterea is not None), 'Undefined value in the filter'
                current_value = s.get(property_name, None)

                if isinstance(filter_criterea, re.Pattern):
                    if not isinstance(current_value, str):
                        return False
                    if not filter_criterea.search(current_value):
                        return False
                if current_value != filter_criterea:
                    return False
            return True
        return matches

    @staticmethod
    def filter(inputs, **filters) -> List[dict]:
        """
            Returns objects with matching fields.
            Supports regular expressions for filtering critereas.
        """
        pred = StatsSubset.predicate(**filters)
        return [s for s in inputs if pred(s)]

    @staticmethod
    def compact(inputs, **aggregation_policies) -> dict:
        """
            Reduces all the dictionaries in this subset by applying
            specified policies to every key in the range.
        """
        if len(inputs) == 0:
            return dict()
        if len(inputs) == 1:
            return inputs[0]

        reduced_dict = dict()
        for aggregated_property, aggregation_policy in aggregation_policies.items():
            all_vals = [s.get(aggregated_property)
                        for s in inputs if aggregated_property in s]
            if len(all_vals) == 0:
                continue
            reduced_val = aggregation_policy(all_vals)
            reduced_dict[aggregated_property] = reduced_val

        return reduced_dict

    @staticmethod
    def group(inputs, *grouping_keys, **aggregation_policies) -> List[dict]:
        """
            Grouping is filtering and compaction chained togethers.
            First we identify all unique combinations of `grouping_keys`.
            For every such combination we group matching stats.
            Once those groups are formed, we `compact()` them into single entries.
        """
        result = list()
        values_per_key = [StatsSubset.get_unique(
            inputs, k) for k in grouping_keys]

        for combo in itertools.product(*values_per_key):
            combo_filter = dict()
            for i, k in enumerate(grouping_keys):
                combo_filter[k] = combo[i]
            matching_stats = StatsSubset.filter(inputs, **combo_filter)
            reduced_stats = StatsSubset.compact(
                matching_stats, **aggregation_policies)
            result.append(reduced_stats)

        return result
