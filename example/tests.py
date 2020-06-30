import math
import random

import pystats2md
from pystats2md.stats_subset import *
from pystats2md.stats_file import *
from pystats2md.micro_bench import *

f = StatsFile('example/tests.json')

assert f.contains(MicroBench(
    benchmark_name='Insert Dump',
    func=lambda: print('RUNNING!!!'),
    database_name='MongoDB',
    dataset='Patent Citations Graph',
    device_name='macbook',
)) == True

assert f.existing_index(MicroBench(
    benchmark_name='Insert Dump',
    func=lambda: print('RUNNING!!!'),
    database_name='MongoDB',
    dataset='Movie Ratings',
    device_name='macbook',
)) == 0

assert f.existing_index(MicroBench(
    benchmark_name='Insert Dump',
    func=lambda: print('RUNNING!!!'),
    database_name='MongoDB',
    dataset='Patent Citations Graph',
    device_name='macbook',
)) == 1

b = MicroBench(
    benchmark_name='Random Sine',
    device_name='macbook',
    func=lambda: math.sin(random.random()),
)
f.upsert(b)
f.dump_to_file()
