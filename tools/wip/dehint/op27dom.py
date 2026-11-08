#!/usr/bin/env python3
"""Attempt 27: attempt 24's dominance argument for e2/e3 checked in the profile_estimate
dump.  gcc 6's call heuristic (predict.c, tree_estimate_probability_bb) predicts edge e
NOT_TAKEN only when e->dest holds a call with side effects, e->src dominates e->dest and
e->dest doesn't post-dominate e->src.  Probes (on today's src/options.c, the rev feed's
C test without its expect, D kept):

  dom    C's true edge to a dead block holding a call (dominated: heuristic expected)
  nodom  C's true edge straight to a live call block it doesn't dominate (the dualboot
         'setting ignored' log, by a label in front of it): no heuristic expected
  nodom2 the same edge to the live rev sprintf (label in front of it; C sits in the
         dualboot block, so it doesn't dominate the sprintf block)

python tools/wip/dehint/op27dom.py [variant ..]  -> the feed tests' predictions"""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import optlib
import op23

SRC = open(optlib.SRC).read()
X = lambda n: '__builtin_constant_p(xb.blSuffix[1] + %d)' % n
C_OLD = 'if (__builtin_expect(%s, 0)) { if (__builtin_expect(%s, 0)) goto dz2; goto dz1; }' % (X(15), X(16))
assert C_OLD in SRC
LOG = '\t\t\t\tlog_printf(1, "dualboot setting ignored!\\n");\n'
assert LOG in SRC, 'log'
SPR = '\t\t\tsprintf(xb.blSuffix, "_%s", s);\n'
assert SPR in SRC, 'sprintf'


def variant(n):
    t = SRC
    if n == 'dom':
        t = t.replace(C_OLD, 'if (%s) { log_printf(1, "x"); if (__builtin_expect(%s, 0)) goto dz2; goto dz1; }' % (X(15), X(16)))
    elif n == 'nodom':
        t = t.replace(LOG, 'ign:\n' + LOG)
        t = t.replace(C_OLD, 'if (%s) goto ign; %s' % (X(17), C_OLD))
    elif n == 'nodom2':
        t = t.replace(SPR, 'rv:\n' + SPR)
        t = t.replace(LOG, '\t\t\t\tif (%s) goto rv;\n' % X(17) + LOG)
    elif n != 'base':
        raise KeyError(n)
    return t


if __name__ == '__main__':
    for n in sys.argv[1:] or ['base', 'dom', 'nodom', 'nodom2']:
        t = variant(n)
        print('==', n, optlib.fmt(optlib.score_text(t)))
        print(op23.preds(t, optlib.P83))
