#!/usr/bin/env python3
"""Attempt 18: the macid memset (ms) is only there so that the validateString test's false
edge reaches a call in its first block (call heuristic 71%); the asm goto (dz1) otherwise
ends that block on its own.  Variants that move the asm goto behind a real call.

python tools/wip/dehint/op18ms.py [variant ..]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SRC = optlib.read_src(optlib.SRC)
MS = '\t\t\t\t\t__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));\n'
AG = '\t\t\t\t\t__asm__ goto ("" :::: dz1);\n'
L1 = '\t\t\t\t\tlog_printf(0, "***** WARNING: invalid characters in macid \'");\n'
SH = '\t\t\t\t\tshowHexPairs(0, s);\n'
L2 = '\t\t\t\t\tlog_printf(0, "\' provided in ini file! Discarding!\\n", s);\n'
BLK = MS + AG + L1 + SH + L2
assert BLK in SRC, 'block'

V = {
    'cur': BLK,
    'noms': AG + L1 + SH + L2,
    'after_l1': L1 + AG + SH + L2,
    'after_sh': L1 + SH + AG + L2,
    'end': L1 + SH + L2 + AG,
}


def main():
    for n in sys.argv[1:] or list(V):
        t = SRC.replace(BLK, V[n], 1)
        print('%-10s %s' % (n, optlib.fmt(optlib.score_text(t))), flush=True)


main()
