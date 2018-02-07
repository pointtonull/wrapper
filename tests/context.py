#!/usr/bin/env python3

"""
Compliant module importer for agnostic testing suite
"""

import sys
from os import path
import importlib

HERE = path.dirname(path.abspath(__file__))
ROOT = path.abspath(path.join(HERE, ".."))
SRC  = path.join(ROOT, "src")

sys.path.insert(0, SRC)

wrapper = importlib.import_module("wrapper", SRC)
