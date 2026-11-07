"""Attempt 50: baseline check of src and each hint off.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a50_base.py -p 99"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
BASE = H.BASE
V = {'src': [], 'pr': [H.PR], 'bar': [H.BAR], 'dev': [H.DEV], 'pin': [H.PIN],
     'lab': [('\t\t\t\tdevgl: __attribute__((hot));\n', '')], 'none': [H.NONE, H.NONE2]}
