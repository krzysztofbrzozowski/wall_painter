from CONSTANTS import *
from loggers import *
import RPiToSTM


class Extruder:

    @classmethod
    def extrude_marker(cls, percentage):
        RPiToSTM.cmd['ext'](percentage)
