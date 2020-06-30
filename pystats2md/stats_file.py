from __future__ import annotations
import json
import csv
from typing import Optional
from os import path
import platform
from datetime import datetime
from pathlib import Path

# from pystats2md.micro_bench import MicroBench
# import pystats2md.stats_file as ss
# from pystats2md.stats_table import StatsTable
import pystats2md.micro_bench as mb
import pystats2md.stats_subset as ss
import pystats2md.stats_table as st


class StatsFile(object):
    """
        Wrapper for the full persistent stats file.
        Can import/produce CSV and JSON (dicts and arrays).
    """

# pragma region Serialization

    def __init__(self, filename=None):
        self.filename = filename
        self.benchmarks = list()
        self.context = dict()
        self.reset_from_file(self.filename)

    def append(self, file: StatsFile):
        self.benchmarks.extend(file.benchmarks)

    def reset_from_file(self, filename=None):
        if filename is None:
            filename = self.filename
            if filename is None:
                return

        if not path.exists(filename):
            self.benchmarks = list()
            self.context = dict()
            return
        with open(filename, 'r') as f:
            ext = Path(filename).suffix
            if ext == '.json':
                self._read_from_json(f)
            elif ext == '.csv':
                self._read_from_csv(f)
            else:
                assert False, f'Unknown extension: {ext}'

    def _read_from_json(self, f):
        contents = json.load(f)
        if isinstance(contents, dict):
            self.context = contents.get('context', dict())
            self.benchmarks = contents.get('benchmarks', list())
            self.benchmarks = [b.update(self.context) for b in self.benchmarks]
        elif isinstance(contents, list):
            self.context = dict()
            self.benchmarks = contents
        else:
            assert False, f'Unknown parsed type: {contents}'

    def _read_from_csv(self, f):
        contents = csv.DictReader(f)
        self.context = dict()
        self.benchmarks = list(contents)

    def dump_to_file(self, filename=None):
        if filename is None:
            filename = self.filename
        with open(filename, 'w') as f:
            ext = Path(filename).suffix
            if ext == '.json':
                self._dump_to_json(f)
            elif ext == '.csv':
                self._dump_to_csv(f)
            else:
                assert False, f'Unknown extension: {ext}'

    def _dump_to_json(self, f):
        json.dump(self.benchmarks, f, indent=4)

    def _dump_to_csv(self, f):
        contents = csv.writer(f)
        if len(self.benchmarks) == 0:
            return

        all_keys = set()
        for b in self.benchmarks:
            for k in b.keys():
                all_keys.add(k)
        all_keys = list(all_keys)
        contents.writerow(all_keys)

        for b in self.benchmarks:
            all_vals = [b.get(k, '') for k in all_keys]
            contents.writerow(all_vals)

    # This is highly unreliable:
    # https://stackoverflow.com/a/29737870/2766161
    # def __del__(self):
    #     self.dump_to_file(self.filename)

# pragma region Modification

    def existing_index(self, bench) -> Optional[int]:
        if isinstance(bench, mb.MicroBench):
            bench = bench.filtering_criterea()
        pred = ss.StatsSubset.predicate(**bench)
        for i, b in enumerate(self.benchmarks):
            if pred(b):
                return i
        return None

    def contains(self, bench) -> bool:
        if isinstance(bench, mb.MicroBench):
            bench = bench.filtering_criterea()
        assert isinstance(bench, dict), type(bench).__name__
        pred = ss.StatsSubset.predicate(**bench)
        for b in self.benchmarks:
            if pred(b):
                return True
        return False

    def __contains__(self, bench) -> bool:
        return self.contains(bench)

    def upsert(self, bench) -> bool:
        """
            Supported types: `str`, `int`, `float`, `datetime.time`.
            Others can be inserted, but won't be queried.
            Returns `True` if the `bench` was inserted as new entry.
            Returns `False` if the `bench` replaced an older entry.
        """
        bench_idx = self.existing_index(bench)

        if isinstance(bench, mb.MicroBench):
            if not self.contains(bench):
                if not bench.did_run():
                    bench.run()
        if not isinstance(bench, dict):
            bench = dict(bench)

        if bench_idx is None:
            self.benchmarks.append(bench)
        else:
            self.benchmarks[bench_idx] = bench

# pragma region Shortcuts

    def subset(self) -> ss.StatsSubset:
        return ss.StatsSubset(source=self)

    def filtered(self, *vargs, **kwargs) -> ss.StatsSubset:
        return ss.StatsSubset(source=self).filtered(*vargs, **kwargs)

    def table(self, rows: str, cols: str, cells: str):
        return ss.StatsSubset(source=self).to_table(
            row_name_property=rows,
            col_name_property=cols,
            cell_content_property=cells,
        )

    def plot(self, *vargs, **kwargs):
        return
