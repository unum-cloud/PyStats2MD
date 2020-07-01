# Exports data from `stats.json` to `stats.md` in human-readable form.
from __future__ import annotations
from typing import List, Optional
import json
import copy
import math
import platform
import inspect
from pathlib import Path
import re

import psutil

from pystats2md.stats_table import StatsTable
from pystats2md.stats_plot import StatsPlot


class Report(object):

    def __init__(self):
        self.clear()

    def clear(self):
        self.content = ''
        self.attachments = {}

    def filename_for(self, filename) -> str:        
        return re.sub('[^\w\-_\.]', '_', filename)

    def print_to(self, filename: str, overwrite=True) -> Report:
        text_file = open(filename, 'w' if overwrite else 'a')
        text_file.write(self.content)
        text_file.close()

        for title, obj in self.attachments.items():
            obj_path = Path(filename).parent / f'{self.filename_for(title)}.svg'
            obj.save_to(str(obj_path))

        self.clear()
        return self

    def add(self, obj: object) -> Report:
        if isinstance(obj, str):
            return self.add_text(obj)
        elif isinstance(obj, StatsTable):
            return self.add_table(obj)
        elif isinstance(obj, StatsPlot):
            return self.add_plot(obj)
        else:
            assert False, 'Unknown type!'
            return self

    def add_text(self, text: str) -> Report:
        assert isinstance(text, str)
        # Remove whitespaces in front of every row.
        # text = '\n'.join([line.strip() for line in text.splitlines()])
        text=inspect.cleandoc(text)
        self.content += f'{text}\n'
        # Headers must have 2 line spacings.
        self.content += '\n\n'
        return self

    def add_table(self, obj: StatsTable) -> Report:
        assert isinstance(obj, StatsTable)
        self.content += obj.print()
        self.content += '\n\n'
        return self

    def add_plot(self, obj: StatsPlot) -> Report:
        assert isinstance(obj, StatsPlot)
        self.attachments[obj.title]=obj
        self.content += '![{}]({}.svg)'.format(
            obj.title,
            self.filename_for(obj.title),
        )
        self.content += '\n\n'
        return self

    def add_current_device_specs(self) -> Report:
        cores=psutil.cpu_count(logical=False)
        threads=psutil.cpu_count(logical=True)
        frequency=psutil.cpu_freq().min
        ram_gbs=psutil.virtual_memory().total / (2 ** 30)
        disk_gbs=psutil.disk_usage('/').total / (2 ** 30)
        self.add(f'''
        * CPU: {cores} cores, {threads} threads @ {frequency:.2f} Mhz.
        * RAM: {ram_gbs:.2f} Gb
        * Disk: {disk_gbs:.2f} Gb
        * OS: {platform.system()}
        ''')
        return self
