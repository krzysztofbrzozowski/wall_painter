import json
import time
from datetime import datetime


class TraceManager:
    def __init__(self):
        self.data = {}
        self.data['people'] = []
        self.data['people'].append({
            'name': 'Scott',
            'website': 'stackabuse.com',
            'from': 'Nebraska'
        })

        self.GCODE_fields = ('G', 'X', 'Y', 'E')

    def value_finder(self):
        pass

    def gcode_parser(self, file):
        pass

    def safe_trace(self):
        with open(f"traces/trace__{datetime.now().strftime('%d_%m_%Y___%H_%M_%S')}.txt", 'w+') as trace_file:
            json.dump(self.data, trace_file)

