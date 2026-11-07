"""Attempt 50: attempt 47's exp_pr spellings again on the post-49 source (shared helpers), alone and
on the equal bases (useNandData kv/kvAlt, notRead).
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a50_neg.py -p 0,95,99"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub
import a50_nand as N
import a50_fail as F

BASE = H.BASE
OLD = 'if (__builtin_expect(r != 0, 0))\n'
SP = {'ne': 'if (r != 0)\n', 'neg': 'if ((int)r < 0)\n', 'm1': 'if (r == (uint32_t)-1)\n', 'le': 'if ((int)r <= -1)\n'}
V = {}
for base in ('src', 'eq'):
    for k, s in SP.items():
        def f(t, base=base, s=s):
            if base == 'eq':
                t = N.mk('ka', 'ka')(t)
                t = F.V['ret_all'](t)
            return sub(t, OLD, s)
        V[base + '_' + k] = f
