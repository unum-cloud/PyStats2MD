from datetime import datetime
import platform
import time
import inspect
import copy

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
        benchmark_name=None,
        device_name=None,
        source=None,
        serialized=None,
        limit_iterations=1000,
        limit_operations=10000,
        limit_seconds=10.0,
        save_context=True,
        save_io=True,
        save_source=True,
        **kwargs,
    ):
        """
            If the provided `func` returns an integer - it's 
            used as `count_operations`.

            The `source` and `serialized` are closely tied. 
            Both allow importing previous results, but `source` 
            also exports the new results back.
        """
        assert callable(func), 'Must be a callable!'
        self.func = func
        self.benchmark_name = benchmark_name if benchmark_name else func.__name__
        self.device_name = device_name if device_name else platform.node()
        self.limit_iterations = limit_iterations
        self.limit_operations = limit_operations
        self.limit_seconds = limit_seconds
        self.save_context = save_context
        self.save_io = save_io
        self.save_source = save_source
        self.attributes = dict(**kwargs)
        self.source = source        
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
            self.attributes.update(serialized)
        elif isinstance(serialized, sf.StatsFile):
            self.deserialize(sf.StatsSubset(source=serialized))
        elif isinstance(serialized, ss.StatsSubset):
            filters = self.filtering_criterea()
            matches = serialized.filter(serialized.dicts_list, **filters)
            if len(matches) > 0:
                self.deserialize(matches[0])

    def context(self) -> dict:
        date = self.date_utc if self.date_utc else datetime.utcnow()
        return {
            # Fields matching Google Benchmark:
            # https://github.com/google/benchmark#output-formats
            'date': date.strftime('%Y/%M/%d-%H:%m:%S'),
            'num_cpus': psutil.cpu_count(),
            'mhz_per_cpu': psutil.cpu_freq().current,
            'build_type': 'debug' if __debug__ else 'release',
            'cpu_scaling_enabled': False,

            # Fields that only we output.
            'device_name': self.device_name,
            'date_utc': datetime.timestamp(date),
            'date_readable': date.strftime('%b %d, %Y'),
            'date_sortable': date.strftime('%Y/%M/%d'),
        }

    def filtering_criterea(self, include_context=False) -> dict:
        result = {
            'benchmark_name': self.benchmark_name,
            'device_name': self.device_name,
        }
        if include_context:
            result.update({
                'num_cpus': psutil.cpu_count(),
                'build_type': 'debug' if __debug__ else 'release',
            })
        result.update(self.attributes)
        return result

    def stats(self) -> dict:
        result = {
            'benchmark_name': self.benchmark_name,
            'time_elapsed': self.time_elapsed,
            'count_iterations': self.count_iterations,
            'count_operations': self.count_operations,
            'msecs_per_operation': self.msecs_per_op(),
            'operations_per_second': self.ops_per_sec(),
        }
        if self.save_source:
            result['benchmark_code'] = inspect.getsource(self.func)
        return result
    
    def current_io(self) -> dict:
        disk = psutil.disk_io_counters()
        net = psutil.net_io_counters()
        return {
            'bytes_sent': net.bytes_sent,
            'bytes_recv': net.bytes_recv,
            'packets_sent': net.packets_sent,
            'packets_recv': net.packets_recv,

            'read_bytes': disk.read_bytes,
            'write_bytes': disk.write_bytes,
            'read_requests': disk.read_count,
            'write_requests': disk.write_count,
        }

    def io(self) -> dict:
        new_io = self.current_io()
        delta_io = {}
        for k, v in self.last_io.items():
            if self.time_elapsed > 0:
                d = new_io[k] - v
                delta_io[k] = d
                delta_io[k + '_per_second'] = d / self.time_elapsed
            else:
                delta_io[k] = 0
                delta_io[k + '_per_second'] = 0
        return delta_io

    def serialize(self) -> dict:
        result = copy.deepcopy(self.attributes)
        result.update(self.stats())
        if self.save_context:
            result.update(self.context())
        if self.save_io:
            result.update(self.io())
        return result

    def __dict__(self) -> dict:
        return self.serialize()

    def __iter__(self) -> dict:
        for k, v in self.serialize().items():
            yield k, v

# pragma region Running

    def run(self):
        before = time.time()
        self.count_operations = 0
        self.count_iterations = 0
        self.last_io = self.current_io()
        while True:
            ops = self.func()

            self.count_operations += ops if isinstance(ops, int) else 1
            self.count_iterations += 1
            self.time_elapsed = time.time() - before

            # Stop if we have reached any limit.
            if self.limit_operations is not None:
                if self.limit_operations <= self.count_operations:
                    break
            if self.limit_iterations is not None:
                if self.limit_iterations <= self.count_iterations:
                    break
            if self.limit_seconds is not None:
                if self.limit_seconds <= self.time_elapsed:
                    break
        # Mark as completed.
        self.date_utc = datetime.utcnow()
        if isinstance(self.source, sf.StatsFile):
            self.source.upsert(self)

    def did_run(self) -> bool:
        return self.date_utc is not None

    def run_if_missing(self):
        if self.did_run():
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

    def secs_per_op(self) -> float:
        if (self.count_operations == 0):
            return 0
        return self.time_elapsed / self.count_operations

    def msecs_per_op(self) -> float:
        if (self.count_operations == 0):
            return 0
        return self.secs_per_op() * 1000.0

    def ops_per_sec(self) -> float:
        if (self.count_operations == 0):
            return 0
        return self.count_operations / self.time_elapsed
