from importlib.machinery import SourceFileLoader

import importlib.util
import sys


MODULE_PATH = '/Users/krzysztofbrzozowski/Documents/PROJECTS/HARDWARE/wall_painter/software/app/gcode_parser.py'
MODULE_NAME = 'GCODEParser'

spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


__version__ = '1.0.0'


def get_gcode_line_values_r(path):
    gcode_parser = module.GCODEParser(path)
    return gcode_parser.get_gcode_line_values()


def get_gcode_lines_amount(path):
    gcode_parser = module.GCODEParser(path)
    return gcode_parser.get_gcode_lines_amount()


if __name__ == '__main__':
    # print(get_gcode_line_values_r('../test_gcode_trace_values.txt'))
    pass
