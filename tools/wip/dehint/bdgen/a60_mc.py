"""Attempt 60: the matches from a60_ub.py (useBuiltIn, devgl label off) crossed with the other hints off
and smcif / smcend.  python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a60_mc.py [-p ..]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a60_ub as U
from a60_est import SMC, SMCIF, SMCEND
V = {}
for k in ('mc_12', 'p_1', 'p_22', 'r_1', 'nest_1', 'mci_12', 'mcz_12'):
    V[k] = U.V[k]
    V[k + '_smcif'] = U.V[k] + [(SMC, SMCIF)]
    V[k + '_smcend'] = U.V[k] + SMCEND
SETS = {k: ['-', 'exp_pr', 'vol_fail', 'exp_devgl'] for k in V}
