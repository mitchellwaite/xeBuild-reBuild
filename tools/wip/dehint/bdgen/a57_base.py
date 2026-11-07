"""Attempt 57: src and each loader hint off (baseline for the structure sweeps).
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a57_base.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
BASE = H.BASE
LAB = ('\t\t\t\tdevgl: __attribute__((hot));\n', '')
V = {'src': [], 'pr': [H.PR], 'bar': [H.BAR], 'lab': [LAB], 'none': [H.NONE, H.NONE2],
     'all4': [H.PR, H.BAR, LAB, H.NONE, H.NONE2]}
