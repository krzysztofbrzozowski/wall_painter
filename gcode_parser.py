import json
import linecache
import os
import sys
from datetime import datetime


class GCODEParser:
    def __init__(self, file):
        if not os.path.isfile(file):
            sys.exit(f'File path {file} does not exist')

        self.file = file

        self.data = {}
        self.GCODE_flds = ('G', 'X', 'Y', 'E')
        self.GCODE_skip = ';'
        self.move_flag = False

        self.gcode_line = 1   # Enumeration start from 1 (sic)

    def set_move_flag(self, value: int):
        self.move_flag = value

    def get_move_flag(self):
        return self.move_flag

    def set_gcode_line(self, value: int):
        self.gcode_line = value

    def inc_gcode_line(self):
        if self.move_flag:
            self.gcode_line += 1

    def get_gcode_line(self):
        return self.gcode_line

    def get_gcode_lines_amount(self):
        with open(self.file) as foo:
            return len(foo.readlines())

    def get_gcode_line_values(self):
        line = linecache.getline(self.file, self.gcode_line)
        cmd_dict = dict()
        for cmd in line.split(' '):
            if self.GCODE_skip in cmd:
                break

            for fld in self.GCODE_flds:
                if fld in cmd:
                    cmd_dict[fld] = int(cmd.replace(fld, ''))

        # cmd_dict = {fld: int(cmd.replace(fld, '')) for fld in self.GCODE_flds for cmd in line.split(' ') if fld in cmd}

        tmp = {'ID': self.gcode_line}
        return {**tmp, **cmd_dict} if len(cmd_dict) else {**cmd_dict}

    @staticmethod
    def safe_trace(data):
        with open(f"traces/trace__{datetime.now().strftime('%d_%m_%Y___%H_%M_%S')}.txt", 'a') as trace_file:
            json.dump(data, trace_file)