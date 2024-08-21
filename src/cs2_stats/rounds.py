"""
Parse a demo into rounds
"""

from demoparser2 import DemoParser

def parse_rounds(parser: DemoParser):
    round_start = parser.parse_event("round_start")
    ticks = parser.parse_ticks()

class Round:
    def __init__(self):
        pass
