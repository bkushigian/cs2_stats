from typing import List
from pynput.keyboard import Controller, Key
from argparse import ArgumentParser
import time
from demoparser2 import DemoParser

class Config:
    def __init__(self, demo_path, player_name):
        self.dp = DemoParser(demo_path)


def run()