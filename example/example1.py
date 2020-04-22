from pystats2md.stats_file import *
from pystats2md.report import *

f = StatsFile('example/benchmarks.json')
r = Report('report.md')

r.add('# Database performance')

r.add(f.table(
    rows='database_name',
    cols='operation_name',
    cells='operations_per_second')
)

r.add(f.chart(
    bars='database_name',
    ys='operations_per_second'
).filter(operation_name='insert'))
