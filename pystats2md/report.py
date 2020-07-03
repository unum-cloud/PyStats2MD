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
import cpuinfo

from pystats2md.stats_table import StatsTable
from pystats2md.stats_plot import StatsPlot
from pystats2md.helpers import *


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
            obj_path = Path(filename).parent / \
                f'{self.filename_for(title)}.svg'
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
        text = inspect.cleandoc(text)
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
        self.attachments[obj.title] = obj
        self.content += '![{}]({}.svg)'.format(
            obj.title,
            self.filename_for(obj.title),
        )
        self.content += '\n\n'
        return self

    def add_current_device_specs(self) -> Report:
        cpu_info = cpuinfo.get_cpu_info()
        cpu_model = cpu_info.get('brand', '?')
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)
        cpu_frequency = metric2str(psutil.cpu_freq().min * 1e6)
        ram_gbs = bytes2str(psutil.virtual_memory().total)
        disk_gbs = bytes2str(psutil.disk_usage('/').total)
        self.add(f'''
        * CPU:
            * Model: `{cpu_model}`.
            * Cores: {cpu_cores} ({cpu_threads} threads @ {cpu_frequency}hz).
        * RAM Space: {ram_gbs}.
        * Disk Space: {disk_gbs}.
        * OS Family: {platform.system()}.
        * Python Version: {platform.sys.version}.
        ''')
        return self
