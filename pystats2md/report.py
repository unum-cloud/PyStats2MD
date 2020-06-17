# Exports data from `stats.json` to `stats.md` in human-readable form.
from __future__ import annotations
from typing import List, Optional
import json
import copy
import math
import platform
import inspect

import psutil

from pystats2md.stats_table import StatsTable
from pystats2md.stats_plot import StatsPlot


class Report(object):

    def __init__(self):
        self.current_content = ''

    def print_to(self, filename: str, overwrite=True) -> Report:
        text_file = open(filename, 'w' if overwrite else 'a')
        text_file.write(self.current_content)
        text_file.close()
        self.current_content = ''
        return self

    def add(self, obj: object) -> Report:
        if isinstance(obj, str):
            return self.add_text(obj)
        elif isinstance(obj, StatsTable):
            return self.add_table(obj)
        elif isinstance(obj, StatsTable):
            return self.add_table(obj)
        else:
            assert False, 'Unknown type!'
            return self

    def add_text(self, text: str) -> Report:
        assert isinstance(text, str)
        # Remove whitespaces in front of every row.
        # text = '\n'.join([line.strip() for line in text.splitlines()])
        text = inspect.cleandoc(text)
        self.current_content += f'{text}\n'
        # Headers must have 2 line spacings.
        self.current_content += '\n\n'
        return self

    def add_table(self, obj: StatsTable) -> Report:
        assert isinstance(obj, StatsTable)
        self.current_content += obj.print()
        self.current_content += '\n\n'
        return self

    def add_plot(self, obj: StatsPlot) -> Report:
        assert isinstance(obj, StatsPlot)
        # filename = random_name()
        # put_into_directory()
        # self.current_content += f'![{obj.name}]({filename})'
        # self.current_content += '\n\n'
        return self

    def add_current_device_specs(self) -> Report:
        cores = psutil.cpu_count(logical=False)
        threads = psutil.cpu_count(logical=True)
        frequency = psutil.cpu_freq().min
        ram_gbs = psutil.virtual_memory().total / (2 ** 30)
        disk_gbs = psutil.disk_usage('/').total / (2 ** 30)
        self.add(f'''
        * CPU: {cores} cores, {threads} threads @ {frequency:.2f} Mhz.
        * RAM: {ram_gbs:.2f} Gb
        * Disk: {disk_gbs:.2f} Gb
        * OS: {platform.system()}
        ''')
        return self
