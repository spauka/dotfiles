#!/usr/bin/env python

# Useful things to have
from __future__ import division
from math import *
import sys, os, re
try:
    from fractions import Fraction
except ImportError:
    pass

__pypy__ = False
try:
    import __pypy__
except ImportError:
    pass

# Readline completion of everything :)
import readline, rlcompleter
if not __pypy__:
    import atexit
    defaultCompleter = rlcompleter.Completer()

    historyPath = os.path.expanduser("~/.pyhistory")

    def myCompleter(text, state):
        if text.strip() == "" and state == 0:
            return text + "\t"
        else:
            return defaultCompleter.complete(text, state)

    def save_history(historyPath=historyPath):
        import readline
        readline.write_history_file(historyPath)

    readline.set_completer(myCompleter)
    readline.parse_and_bind("tab: complete")

    if os.path.exists(historyPath):
        readline.read_history_file(historyPath)

    atexit.register(save_history)

    del rlcompleter, readline, atexit
else:
    readline.parse_and_bind("tab: complete")
