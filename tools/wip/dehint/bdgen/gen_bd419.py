"""Attempt 30: gen_bd418's lead.  On case 6 first + and9 + c2 (fail closing case 2) the barrier costs 1 loose / 7 strict:
only the size log's own `mov edi,-1`.  Sweep the case order around it (every arm to every place, from the c6 order) with
the barrier off, and the size error's forms (src's goto fail, its own `*pr = -1; break;`).  Runs on src as of 6083630d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun, bdhints
import a30lib
import gen_bd418 as g8
import gen_bd417 as g7

SZ = '''			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			goto fail;
'''
SZO = '''			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			*pr = -1;
			break;
'''


def mk(b, o, sz):
    b = g8.base(b, 'c2c6')
    b = bdhints.off(b, 'vol_fail')
    if o is not None:
        b = g7.reorder(b, o)
    if sz:
        b = bdrun.sub(b, SZ, SZO, 1)
    return b


def CASES(base):
    b = g8.base(base, 'c2c6')
    i, j = bdrun.fnspan(b, a30lib.LB)
    h, a, t = g7.arms(b[i:j])
    n = g7.names(a)
    orders = {'c6': None}
    for k in range(len(n)):
        for p in range(len(n) + 1):
            if p == k or p == k + 1:
                continue
            o = list(n)
            x = o.pop(k)
            o.insert(p if p < k else p - 1, x)
            orders['mv %s@%d' % (n[k], p)] = o
    return [('%s %d' % (lab, sz), lambda b, o=o, sz=sz: mk(b, o, sz)) for (lab, o), sz in itertools.product(orders.items(), [0, 1])]


FOCUS = ['_loadBlFiles']
