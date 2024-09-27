"""
Framework for creating a bot for Hackaton 2024
----------------------------------------------

This module provides a framework for creating a bot for Hackaton 2024.
The main class is `HackatonBot`, which should be subclassed and implemented
with the required methods.
"""

__title__ = "HackArena2024H2-Python"
__author__ = "KN __init__"
__copyright__ = "2024 KN __init__"
__license__ = "MIT"
__version__ = "0.1.0"

from .actions import *
from .enums import *
from .hackaton_bot import HackatonBot
from .protocols import *
