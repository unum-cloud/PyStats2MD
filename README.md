# PyStats2MD

A simple library to export benchmark results, compatiable with [Google Benchmark](https://github.com/google/benchmark) CSV and JSON output formats. Allows building nice markdown tables and charts in just a few lines of code.

## Features

* Filtering and grouping data from benchmarks files.
* Rendering GitHub-Markdown tables with easy formatting.
* Generating and embedding plots with `matplotlib` in just a couple of lines.
* Included pure-Python benchmarking tool with same output file formats as Google Benchmark.
* Lets you embed the source code of benchmarked Python function into the Markdown report!

## Installation

```sh
pip install pystats2md
```

## Examples

### Example 1

Let's assume we are benchmarking databases. We have an array of measurements and each of them is a dictionary with at least 3 keys: `database_name`, `operation_name` and `operations_per_second`. Let's generate a report.

```python
from pystats2md import *

f = StatsFile('benchmarks.json')
r = Report('report.md')
r.add('#### Following section was auto-generated')
r.add(f.table(rows='database_name', cols='operation_name', cells='operations_per_second'))
r.add(f.chart(bars='database_name', ys='operations_per_second').filter(operation_name='insert'))
```

### Example 2

A more complex example. The [previous example](#example-1) assumes we have just 1 entry for every combination of `database_name`, `operation_name`. If it's not the case, we can reduce them in-place and also add all kinds of supplementary columns to make results more visually appealing. Just don't get carried away :laughing: 

```python
r.add('#### Following section was auto-generated')
r.add(f
    .group('database_name', 'operation_name', { 'operations_per_second': Aggregation.take_mean }) \
    .table(rows='database_name', cols='operation_name', cells='operations_per_second') \
    .add_ranking(column='insert') \
    .add_emoji(column='insert', log_scale=False) \
    .add_gains(column='insert', baseline='SQLite')
)
# If no context is specified in the input file - we will generate one on the fly - assuming it's the same device.
r.add(f.benchmark_context())
# If no date is found in the context - we will search for the biggest timestamp in the input file.
r.add(f.timestamp('timestamp_utc'))
```

### Example 3

If you need even more control, you can manually build `StatsSubset` from `StatsFile` and export it into `StatsPlot` or `StatsTable`.

## Related Projects

* [PyGraphDB](https://github.com/unumxyz/PyGraphDB) lib for persistent graph data structures.
* [Unum](https://unum.xyz) high-performance GPU-accelerated general-purpose framework.

## TODO

- [ ] Plot generation.
- [ ] Add option to highlight biggest/smallest value per column as bold.
- [ ] Add special `class MeanAndStdev` which when rendered shows the standard deviation of preceding reduction. 
- [ ] Add inline HTML color-coding for standard deviation size.
- [ ] Add astriks and subtitles for results that have much older timestamps.