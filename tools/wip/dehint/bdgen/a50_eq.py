"""Attempt 50: attempt 50's equal bases together (useNandData at kv/kvAlt in both loaders, notRead),
each hint off, for the param sweep.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a50_eq.py -p 0,90,95,99"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub, OFF
import a50_nand as N
import a50_fail as F

BASE = H.BASE
V = {}
for k in ('all', 'pr', 'lab', 'none', 'bar', 'dev'):
    def f(t, p=OFF[k]):
        t = N.mk('ka', 'ka')(t)
        t = F.V['ret_all'](t)
        for a, c in p:
            t = sub(t, a, c)
        return t
    V['eq_' + k] = f
