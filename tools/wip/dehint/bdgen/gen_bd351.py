"""Attempt 24, attempt 24's assert-order lever on loadBl: the signature test's leaf order (which leaf is the lone
GIMPLE_COND and which pair is folded, so which `!=`/`==` asserts vrp1's threader sees on each edge), crossed with
loadBl's hints off (t5le, exp_pr, exp_t10, the dead `else if (type)`, the barrier).  Attempt 18's gen_bd294 swept the
orders with t5le off only.  Runs on src as of 892a28f1 + attempt 24's landing."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun, bdhints

SIG = 'if (type == 5 || type == 17 || type == 11) {'
ORD = ['5 17 11', '17 5 11', '11 5 17', '11 17 5', '5 11 17', '17 11 5']
DEAD = ('				} else if (type)\n', '				} else\n')
OFF = {'-': [], 't5le': ['lab_t5le'], 'pr': ['exp_pr'], 't5le,pr': ['lab_t5le', 'exp_pr'], 't10': ['exp_t10'],
       'dead': 'dead', 'fail': ['vol_fail'], 't5le,pr,dead': ['lab_t5le', 'exp_pr', 'dead']}


def mk(t, o, off):
    a, b, c = o.split()
    t = bdrun.sub(t, SIG, 'if (type == %s || type == %s || type == %s) {' % (a, b, c), 1)
    names = OFF[off] if OFF[off] != 'dead' else ['dead']
    for n in names:
        if n == 'dead':
            t = bdrun.sub(t, DEAD[0], DEAD[1], 1)
        else:
            t = bdhints.off(t, n)
    return t


def CASES(base):
    out = []
    for o, off in itertools.product(ORD, OFF):
        out.append(('%s | %s' % (o, off), lambda b, o=o, off=off: mk(b, o, off)))
    return out


FOCUS = ['_loadBlFiles']
