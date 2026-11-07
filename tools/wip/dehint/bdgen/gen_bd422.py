"""Attempt 30, pin_d: IRA's pop order between case 27's base and d (attempt 16) may break ties by pseudo number, which
expand order sets; the case order changes expand order without changing GIMPLE.  Every arm moved to every place (from
src's order and from the case-6-first order) with pin_d off and every other hint kept; also on the and9 + c2 base.
Runs on src as of 6083630d."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun, bdhints
import a30lib
import gen_bd410 as g0
import gen_bd417 as g7


def CASES(base):
    i, j = bdrun.fnspan(base, a30lib.LB)
    h, a, t = g7.arms(base[i:j])
    n = g7.names(a)
    orders = {'src': n}
    for k in range(len(n)):
        for p in range(len(n) + 1):
            if p == k or p == k + 1:
                continue
            o = list(n)
            x = o.pop(k)
            o.insert(p if p < k else p - 1, x)
            orders['mv %s@%d' % (n[k], p)] = o
    c = []
    for lab, o in orders.items():
        c.append(('src ' + lab, lambda b, o=o: bdhints.off(g7.reorder(b, o), 'pin_d')))
        c.append(('c2 ' + lab, lambda b, o=o: bdhints.off(g7.reorder(g0.and9c2(b), o), 'pin_d')))
    return c


FOCUS = ['_loadBlFiles']
