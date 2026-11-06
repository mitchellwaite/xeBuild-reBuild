"""Attempt 3: macid's memset feed.  The memset(s, 0, cp) keeps PRED_CALL on the edge into the
asm goto's block (the call folds away); a real call before the asm goto would do the same.
Variants move the asm goto after each of the arm's calls, with the memset dropped.

python tools/wip/dehint/opmac3.py"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

MS = '\t\t\t\t\t\t__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));\n'
AG = '\t\t\t\t\t\t__asm__ goto ("" :::: dz1);\n'
L1 = '\t\t\t\t\t\tlog_printf(0, "***** WARNING: invalid characters in macid \'");\n'
SH = '\t\t\t\t\t\tshowHexPairs(0, s);\n'
L2 = '\t\t\t\t\t\tlog_printf(0, "\' provided in ini file! Discarding!\\n", s);\n'
MS, AG, L1, SH, L2 = (x[1:] for x in (MS, AG, L1, SH, L2))  # five tabs in src
ARM = MS + AG + L1 + SH + L2


def src():
    t = optlib.read_src(optlib.SRC)
    assert ARM in t
    return t


V = {
    'ms_only': ARM.replace(MS, ''),
    'after_l1': L1 + AG + SH + L2,
    'after_sh': L1 + SH + AG + L2,
    'after_l2': L1 + SH + L2 + AG,
    'ms_after_l1': MS.replace('9', '9') and L1 + MS + AG + SH + L2,
}


def run(n):
    return n, optlib.fmt(optlib.score_text(src().replace(ARM, V[n])))


if __name__ == '__main__':
    with ThreadPoolExecutor(6) as ex:
        for n, r in ex.map(run, sys.argv[1:] or list(V)):
            print(n, r[:200])
