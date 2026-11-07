"""Attempt 52: src and pin_size / exp_devgl off (sanity).
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a52_base.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
BASE = H.BASE
V = {'src': [], 'pin': [H.PIN], 'dev': [H.DEV], 'pindev': [H.PIN, H.DEV]}
