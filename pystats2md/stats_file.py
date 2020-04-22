import json
from typing import Optional
from os import path
import platform
from datetime import datetime

import psutil


class StatsFile(object):

    def __init__(self, filename='tmp/stats.json'):
        self.filename = filename
        self.benchmarks = list()
        self.context = dict()
        self.reset_from_file(self.filename)

    # This is highly unreliable:
    # https://stackoverflow.com/a/29737870/2766161
    # def __del__(self):
    #     self.dump_to_file(self.filename)

    def contains(self, **kwargs) -> bool:
        matches = StatsSubset().filter(self.stream())
        return len(matches) == 0

    def find_index(
        self,
        wrapper_class: str,
        operation_name: str,
        dataset: str = '',
    ) -> Optional[int]:
        for i, r in enumerate(self.benchmarks):
            if self.bench_matches(r, wrapper_class, operation_name, dataset):
                return i
        return None

    def upsert(self, **kwargs):
        """
            Supported types: `str`, `int`, `float`, `datetime.time`.
            Others can be inserted, but won't be queried.
        """

        bench_idx = self.find_index(wrapper_class, operation_name, dataset)
        stats_serialized = {
            'device': self.device_name,
            'time_elapsed': stats.time_elapsed,
            'count_operations': stats.count_operations,
            'msecs_per_operation': stats.msecs_per_op(),
            'operations_per_second': stats.ops_per_sec(),
            'operation': operation_name,
            'database': wrapper_class,
            'dataset': dataset,
            'date_utc': datetime.timestamp(datetime.utcnow()),
            'date_readable': datetime.utcnow().strftime("%b %d, %Y"),
            'date_sortable': datetime.utcnow().strftime("%Y/%M/%d"),
        }
        if bench_idx is None:
            self.benchmarks.append(stats_serialized)
        else:
            self.benchmarks[bench_idx] = stats_serialized

    def reset_from_file(self, filename=None):
        if filename is None:
            filename = self.filename
        if not path.exists(filename):
            self.benchmarks = []
            self.context = self.make_context()
            return
        with open(filename, 'r') as f:
            self._read_from_json(f)

    def _read_from_json(self, f):
        contents = json.load(f)
        if isinstance(contents, dict):
            self.context = contents.get('context', dict())
            self.benchmarks = contents.get('benchmarks', list())
        elif isinstance(contents, list):
            self.context = self.make_context()
            self.benchmarks = contents
        else:
            assert False, f'Unknown parsed type: {contents}'

    def _read_from_csv(self, f):
        pass

    def make_context(self) -> dict:
        return {
            'device': platform.name
        }

    def dump_to_file(self, filename=None):
        if filename is None:
            filename = self.filename
        with open(filename, 'w') as f:
            json.dump(self.benchmarks, f, indent=4)

    def import_file(self, source: str) -> StatsSubset:
        contents = json.load(open(source, 'r'))
        assert isinstance(contents, list), 'Must be a list!'
        assert len(contents) > 0, 'Shouldnt be empty!'
        self.dicts_list.extend(contents)
        return self

    # pragma mark - Shortcuts
    def table(self, *vargs, **kwargs):
        return
