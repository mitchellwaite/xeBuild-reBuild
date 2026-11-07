"""Attempt 30: gen_bd411's best structures (c2, and9/src, ptr/retu, src/nk sig) with `else if (type)` put back on the
passed log (diagnostic: how much is etype's alone on each structure), and with the type-11 entry / t5le / exp_pr hints
back one at a time.  Runs on src as of 6083630d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
import gen_bd411 as g

PASSED = g.PASSED


def dead(f, sig):
    if sig in ('src',):
        return bdrun.sub(f, '\t\t\t\t} else\n\t\t\t\t\t' + PASSED, '\t\t\t\t} else if (type)\n\t\t\t\t\t' + PASSED, 1)
    if sig == 'nk':
        return bdrun.sub(f, '\t\t\t} else\n\t\t\t\t' + PASSED, '\t\t\t} else if (type)\n\t\t\t\t' + PASSED, 1)
    if sig == 'nkp':
        return bdrun.sub(f, '\t\t\telse if (cbVerifySig(e->data, xb.pub1bl))\n\t\t\t\t' + PASSED,
                         '\t\t\telse if (cbVerifySig(e->data, xb.pub1bl)) {\n\t\t\t\tif (type)\n\t\t\t\t\t' + PASSED + '\n\t\t\t}', 1)
    return None


def mk(b, res, fb, sig, tail, d):
    t = g.mk(b, res, fb, 'c2', sig, tail)
    if t is None:
        return None
    if d:
        t = dead(t, sig)
    return t


PRE = g.PRE


def CASES(base):
    return [(' '.join(map(str, k)), lambda b, k=k: mk(b, *k))
            for k in itertools.product(['ptr', 'retu'], ['src', 'and9'], ['src', 'nk', 'nkp'], ['src', 'plain'], [0, 1])]


FOCUS = ['_loadBlFiles']
