from datetime import datetime
import platform
import time
import inspect

import psutil

import pystats2md.stats_file as sf
import pystats2md.stats_file as ss


class MicroBench(object):
    """
        A single benchmark, that can be attached to a persistent file.
        In that case we can avoid re-running big benchmarks, if previous
        results for the same configuration exists.
        Allows batching multiple operations in the same iteration and logs both.
    """

# pragma region Serialization

    def __init__(
        self,
        func,
        name=None,
        device_name=None,
        serialized=None,
        limit_iterations=1000,
        limit_operations=10000,
        limit_seconds=1.0,
    ):
        """
            If the provided `func` returns an integer - it's used as `count_operations`.
        """
        assert callable(func), 'Must be a callable!'
        self.func = func
        self.benchmark_name = name if name else func.__name__
        self.device_name = device_name if device_name else platform.node()
        self.limit_iterations = limit_iterations
        self.limit_operations = limit_operations
        self.limit_seconds = limit_seconds
        self.deserialize(serialized)

    def deserialize(self, serialized):
        if serialized is None:
            self.time_elapsed = 0
            self.count_operations = 0
            self.count_iterations = 0
            self.date_utc = None
        elif isinstance(serialized, dict):
            self.time_elapsed = serialized['time_elapsed']
            self.count_operations = serialized['count_operations']
            self.count_iterations = serialized['count_iterations']
            self.date_utc = datetime.fromtimestamp(serialized['date_utc'])
        elif isinstance(serialized, sf.StatsFile):
            self.deserialize(sf.StatsSubset(source=serialized))
        elif isinstance(serialized, ss.StatsSubset):
            filters = self.filtering_predicate()
            matches = serialized.filter(serialized.dicts_list, **filters)
            if len(matches) > 0:
                self.deserialize(matches[0])

    def context(self) -> dict:
        date = self.date_utc if self.date_utc else datetime.utcnow()
        return {
            # Fields matching Google Benchmark:
            # https://github.com/google/benchmark#output-formats
            'date': date.strftime('%Y/%M/%d-%H:%m:%s'),
            'num_cpus': psutil.cpu_count(),
            'mhz_per_cpu': psutil.cpu_freq().current,
            'build_type': 'debug' if __debug__ else 'release',
            'cpu_scaling_enabled': False,

            # Fields that only we output.
            'device': self.device_name,
            'date_utc': datetime.timestamp(date),
            'date_readable': date.strftime('%b %d, %Y'),
            'date_sortable': date.strftime('%Y/%M/%d'),
        }

    def filtering_predicate(self) -> dict:
        return {
            'benchmark_name': self.benchmark_name,
            'device': self.device_name,
            # Parts of context:
            'num_cpus': psutil.cpu_count(),
            'build_type': 'debug' if __debug__ else 'release',
        }

    def serialize(self) -> dict:
        return {
            'benchmark_name': self.benchmark_name,
            'benchmark_code': inspect.getsource(self.func),
            'time_elapsed': self.time_elapsed,
            'count_iterations': self.count_iterations,
            'count_operations': self.count_operations,
            'msecs_per_operation': self.msecs_per_op(),
            'operations_per_second': self.ops_per_sec(),
        }.update(self.context())

    def __dict__(self) -> dict:
        return self.serialize()

# pragma region Running

    def run(self):
        before = time.time()
        self.count_operations = 0
        self.count_iterations = 0
        while True:
            ops = self.func()

            self.count_operations += ops if isinstance(ops, int) else 1
            self.count_iterations += 1
            self.time_elapsed = time.time() - before

            # Stop if we have reached any limit.
            if self.limit_operations:
                if self.limit_operations <= self.count_operations:
                    break
            if self.limit_iterations:
                if self.limit_iterations <= self.count_iterations:
                    break
            if self.limit_seconds:
                if self.limit_seconds <= self.time_elapsed:
                    break
        # Mark as completed.
        self.date_utc = datetime.utcnow()

    def run_if_missing(self):
        if self.date_utc is not None:
            return
        self.run()

    def __call__(self):
        return self.run()

# pragma region Logging

    def __repr__(self) -> str:
        n = self.benchmark_name
        o = '%.1E' % self.count_operations
        t = '%.2E' % self.msecs_per_op()
        return f'<MicroBench: {n} (#{o} ops × {t} msecs)>'

    def __str__(self) -> str:
        """
            Prints in format similar to Google Benchmark:
            ------------------------------------------------------------------------
            Benchmark                              Time      Operations   Iterations
            ------------------------------------------------------------------------
        """
        n = '%34.34s' % self.benchmark_name
        t_mili = self.msecs_per_op()
        t = '%.1f ms' % t_mili
        if t_mili < 1.0:
            t = '%.1f ns' % (t_mili * 1000.0)
        elif t_mili > 1000.0:
            t = '%.1f s' % (t_mili / 1000.0)
        t = '%10.10s' % t
        o = '%13.13s' % str(self.count_operations)
        i = '%13.13s' % str(self.count_iterations)
        return f'{n}{t}{o}{i}'

    @property
    def secs_per_op(self) -> float:
        if (self.count_operations == 0):
            return 0
        return self.time_elapsed / self.count_operations

    @property
    def msecs_per_op(self) -> float:
        if (self.count_operations == 0):
            return 0
        return self.secs_per_op() * 1000.0

    @property
    def ops_per_sec(self) -> float:
        if (self.count_operations == 0):
            return 0
        return self.count_operations / self.time_elapsed
