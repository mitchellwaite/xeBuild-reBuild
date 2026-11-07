"""Attempt 40: attempt 39's `edata` (the tail reads e->data) lets loadBl drop its `i` parameter once the constant_p entry
stops naming i.  Forms of the entry's first term without i: e, *pr's address, e->crc, e->size, e->data, type alone
(`(char *)__builtin_constant_p(X) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1`), with and without
dropping i from the signature, crossed with gen_bd510's offs.  Runs on src as of 53c5fc43.
`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd521.py`."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
from gen_bd510 import LB_HEAD, lbf, off, edata, OFFS

FOCUS = ['_loadBlFiles']
CP = '(char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1'


def noi(t):
    t = bdrun.sub(t, LB_HEAD, LB_HEAD.replace('uint32_t i, ', ''), 1)
    return lbf(t, 'loadBl(e, i, &r);', 'loadBl(e, &r);')


def cpf(t, x):
    if x is None:
        return bdrun.sub(t, CP, '(char *)__builtin_constant_p(type) == (char *)1')
    return bdrun.sub(t, CP, CP.replace('(i)', '(%s)' % x))


VARIANTS = {'src': lambda t: t, 'edata': edata}
for nm, x in (('e', 'e'), ('crc', 'e->crc'), ('size', 'e->size'), ('data', 'e->data'), ('t', None), ('off', 'e->offset')):
    VARIANTS['ed_' + nm] = lambda t, x=x: cpf(edata(t), x)
    VARIANTS['noi_' + nm] = lambda t, x=x: noi(cpf(edata(t), x))

OFFS2 = [k for k in OFFS if k != 'cp']


def CASES(base):
    return [('%s|%s' % (v, k), lambda b, f=f, k=k: off(f(b), k)) for v, f in VARIANTS.items() for k in OFFS2]
