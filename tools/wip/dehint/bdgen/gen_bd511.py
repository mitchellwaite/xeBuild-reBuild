"""Attempt 39: narrow types for loadBl's `type` local (attempt 33's gen_bd450 only tried int / uint32_t / unsigned):
uint8_t, uint16_t, signed char, short, and the same with the SE store kept on e->type.  VRP then knows the range
from the type, which changes the switch's range test and the predictors on the 9 / 10 / SE / 5-17-11 tests.
Crossed with every loadBl-side trick off alone (gen_bd510's off()).  Runs on src as of a9cb46e0.
`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd511.py`."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
from gen_bd510 import LB_HEAD, off, OFFS

FOCUS = ['_loadBlFiles']


def ty(t, n):
    return bdrun.sub(t, LB_HEAD, LB_HEAD.replace('\tint type;', '\t%s type;' % n), 1)


VARIANTS = {k: (lambda t, k=k: ty(t, k)) for k in ('uint8_t', 'uint16_t', 'signed char', 'short', 'int8_t', 'int16_t')}


def CASES(base):
    return [('%s|%s' % (v, k), lambda b, f=f, k=k: off(f(b), k)) for v, f in VARIANTS.items() for k in OFFS]
