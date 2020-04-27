import pystats2md
from pystats2md.stats_file import *
from pystats2md.report import *

f = StatsFile('example/benchmarks.json')
r = Report()

r.add('# Database performance')

r.add(f.table(
    rows='database_name',
    cols='benchmark_name',
    cells='operations_per_second',
))

# r.add(f.chart(
#     bars='database_name',
#     ys='operations_per_second',
# ).filter(
#     benchmark_name='insert',
# ))

r.print_to('example/example1.md')
