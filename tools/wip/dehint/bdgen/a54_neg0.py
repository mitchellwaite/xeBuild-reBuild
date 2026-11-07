"""Attempt 54: baseline, exp_pr as `(int)r < 0` on src.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a54_neg0.py -p 0,99 -k neg"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
BASE = H.BASE
V = {'src': [], 'neg': [('if (__builtin_expect(r != 0, 0))\n', 'if ((int)r < 0)\n')]}
