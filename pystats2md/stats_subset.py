import copy
import re  # Filtering
import itertools  # Combinations of grouping keys

from pystats2md.helpers import *
from pystats2md.stats_table import StatsTable
from pystats2md.aggregation import Aggregation
from pystats2md.file import StatsFile


class StatsSubset(object):

    def __init__(self, source=None):
        self.dicts_list = list()

    def include(self, contents: List[dict]) -> StatsSubset:
        if isinstance(contents, list):
            self.dicts_list.extend(copy.deepcopy(contents))
            return self
        elif isinstance(contents, StatsFile):
            self.dicts_list.extend(contents.copy())
            return self
        elif isinstance(contents, str):
            contents = StatsFile(contents)
            self.dicts_list.extend(contents.copy())
            return self

    def filtered(self, **filters) -> StatsSubset:
        self.dicts_list = self.filter(self.dicts_list, **filters)
        return self

    def compacted(self, **aggregation_policies) -> StatsSubset:
        self.dicts_list = self.compact(self.dicts_list, **aggregation_policies)
        return self

    def grouped(self, *grouping_keys, **aggregation_policies) -> StatsSubset:
        self.dicts_list = self.group(
            self.dicts_list, *grouping_keys, **aggregation_policies)
        return self

    def unique_strings_for(self, inputs, key: str) -> Set[str]:
        return {num2str(s.get(key)) for s in inputs if key in s}

    def to_table(
        self,
        row_name_property: str,
        col_name_property: str,
        cell_content_property: str,
        row_names: List[str],
        col_names: List[str],
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

        if len(row_names == 0):
            row_names = self.unique_strings_for(
                self.dicts_list, row_name_property)
        if len(col_names == 0):
            col_names = self.unique_strings_for(
                self.dicts_list, col_name_property)

        result = [[''] * len(col_names)] * len(row_names)
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
        return StatsTable(content=result, header_row=col_names, header_col=row_names)

    def filter(self, inputs, **filters) -> List[dict]:
        """
            Returns objects with matching fields.
            Supports regular expressions for filtering critereas.
        """
        # Define filtering predicate.
        def matches(s: dict) -> bool:
            for filtered_prpoperty, filter_criterea in filters.items():
                assert (
                    filtered_prpoperty is not None), 'Undefined key in the filter'
                assert (filter_criterea is not None), 'Undefined value in the filter'
                current_value = s.get(filtered_prpoperty, None)
                if isinstance(filter_criterea, re.Pattern):
                    if (not filter_criterea.search(current_value)) or \
                            (not isinstance(current_value, str)):
                        return False
                elif current_value != filter_criterea:
                    return False
            return True
        # Actual filtering.
        return [s for s in inputs if matches(s)]

    def compact(self, inputs, **aggregation_policies) -> dict:
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

    def group(self, inputs, *grouping_keys, **aggregation_policies) -> List[dict]:
        """
            Grouping is filtering and compaction chained togethers.
            First we identify all unique combinations of `grouping_keys`.
            For every such combination we group matching stats.
            Once those groups are formed, we `compact()` them into single entries.
        """
        result = list()
        values_per_key = [self.unique_strings_for(
            inputs, k) for k in grouping_keys]

        for combo in itertools.product(*values_per_key):
            combo_filter = dict()
            for i, k in enumerate(grouping_keys):
                combo_filter[k] = combo[i]
            matching_stats = self.filter(inputs, **combo_filter)
            reduced_stats = self.compact(
                matching_stats, **aggregation_policies)
            result.append(reduced_stats)

        return result
