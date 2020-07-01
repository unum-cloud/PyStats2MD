# pystats2md

A simple library to export benchmark results, compatiable with [Google Benchmark](https://github.com/google/benchmark) CSV and JSON output formats. Allows building nice markdown tables and charts in just a few lines of code.

## Features

* Filtering and grouping data from benchmarks files.
* Rendering GitHub-Markdown tables with easy formatting.
* Generating and embedding plots with [Plotly](https://plotly.com) in just a couple of lines.
* Included pure-Python benchmarking tool with same output file formats as Google Benchmark.
* Embeds the source code of the benchmark itself into the log files and reports!

## Installation

```sh
pip install pystats2md
```

## Examples

### Example 1

Let's assume we are benchmarking databases. We have an array of measurements and each of them is a dictionary with at least 3 keys: `database_name`, `benchmark_name` and `operations_per_second`. Let's generate a report.

```python
from pystats2md import *

f = StatsFile('benchmarks.json')
r = Report()
r.add('#### Following section was auto-generated')
r.add(f.table(
    rows='database_name', 
    cols='benchmark_name', 
    cells='operations_per_second'
))
r.add(f.plot(
    title='DB Performance (Ops/Sec)', 
    variants='database_name', 
    groups='benchmark_name', 
    values='operations_per_second'
))
r.print_to('example/README.md')
```

![DB Performance (Ops/Sec)](example/DB_Performance__Ops_Sec_.svg)

### Example 2

A more complex example. The [previous example](#example-1) assumes we have just 1 entry for every combination of `database_name`, `benchmark_name`. If it's not the case, we can reduce them in-place and also add all kinds of supplementary columns to make results more visually appealing. Just don't get carried away :laughing: 

```python
r.add('#### Following section was auto-generated')
r.add(f \
    .subset() \
    .group('database_name', 'benchmark_name', **{ 'operations_per_second': Aggregation.take_mean }) \
    .table(rows='database_name', cols='benchmark_name', cells='operations_per_second') \
    .add_ranking(column='insert') \
    .add_emoji(column='insert', log_scale=False) \
    .add_gains(column='insert', baseline='SQLite')
)
# If no context is specified in the input file - we will generate one on the fly - assuming it's the same device.
r.add_current_device_specs()
```

### Example 3

If you need even more control, you can manually build `StatsSubset` from `StatsFile` and export it into `StatsPlot` or `StatsTable`.
Such workflows can be found [here](example).

## Related Projects

* [PyWrappedDBs](https://github.com/unumxyz/PyWrappedDBs) lib for persistent graph data structures us `pystats2md` to render reports.
* [Unum](https://unum.xyz) high-performance GPU-accelerated general-purpose framework.

## TODO

- [ ] Add special `class MeanAndStdev` which when rendered shows the standard deviation of preceding reduction. 
- [ ] Add inline HTML color-coding for standard deviation size.
- [ ] Add astriks and subtitles for results that have much older timestamps.