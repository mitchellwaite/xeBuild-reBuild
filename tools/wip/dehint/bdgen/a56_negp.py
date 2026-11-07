"""Attempt 56: exp_pr's `(int)r < 0` and `r != 0` with and without the barrier on attempt 55's SMC
`if` base, for a param sweep.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a56_negp.py -p 0,80,85,90,95,96,97,98,99"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
import a55_smc as S
BASE = H.BASE
NEG = ('if (__builtin_expect(r != 0, 0))\n', 'if ((int)r < 0)\n')
V = {}
for bar in (1, 0):
    for k, ed in (('exp', []), ('pr', [H.PR]), ('neg', [NEG])):
        V['if_%s_%s' % ('b' if bar else 'nb', k)] = S.smcif(bar) + ed
