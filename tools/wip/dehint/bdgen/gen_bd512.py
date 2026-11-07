"""Attempt 39: where chk's type comes from: the field instead of the local.  After `chk:` the code reads e->type
(reloaded after loadInputFile / suGetCF / suGetCG, so vrp1 no longer knows a constant type on the paths into the
shared checkBl copy, which is what the constant_p entry and exp_t10 are about).  Same behaviour: e->type is the
local's value at chk on every path (the SE arm stores both).  Forms: `rl` a reload `type = e->type;` right after
the label; `fld` every use after chk spelled e->type; `fld_ck` only checkBl's argument; `fld_tail` only the tests
after checkBl.  Crossed with gen_bd510's offs plus `cp+exp_t10`.  Runs on src as of a9cb46e0.
`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd512.py`."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
from gen_bd510 import off, OFFS

FOCUS = ['_loadBlFiles']

CHK = '\tchk:\n\t\t*pr = checkBl(e->data, e->size, type, e->crc);\n'
TESTS = [('\t\tif (type == 5 || type == 17 || type == 11) {\n', '\t\tif (e->type == 5 || e->type == 17 || e->type == 11) {\n'),
         ('\t\t\t\t} else if (type)\n', '\t\t\t\t} else if (e->type)\n'),
         ('\t\tif (type == 14)\n\t\t\tsetFlashBuild', '\t\tif (e->type == 14)\n\t\t\tsetFlashBuild')]


def rl(t):
    return bdrun.sub(t, CHK, '\tchk:\n\t\ttype = e->type;\n\t\t*pr = checkBl(e->data, e->size, type, e->crc);\n', 1)


def ck(t):
    return bdrun.sub(t, CHK, CHK.replace(', type,', ', e->type,'), 1)


def tail(t, which=(0, 1, 2)):
    for k in which:
        t = bdrun.sub(t, *TESTS[k], count=1)
    return t


VARIANTS = {
    'rl': rl,
    'fld': lambda t: tail(ck(t)),
    'fld_ck': ck,
    'fld_tail': tail,
    'fld_t0': lambda t: tail(t, (0,)),
    'fld_t2': lambda t: tail(t, (2,)),
}


def off2(t, k):
    for x in k.split('+'):
        t = off(t, x)
    return t


def CASES(base):
    return [('%s|%s' % (v, k), lambda b, f=f, k=k: off2(f(b), k)) for v, f in VARIANTS.items() for k in OFFS + ['cp+exp_t10']]
