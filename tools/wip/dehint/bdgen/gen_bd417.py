"""Attempt 30: the switch's case order in loadBl.  Every arm moved to every other position (from src's order), plus the
numeric order and the .rdata-implied order, each with every hint kept (an equally matching base?) and with the seven
loadBl hints off (a30lib.off7).  Arms are cut at the one-tab `case`/`default` lines.  Runs on src as of 6083630d."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
from a30lib import off7, LB


def arms(f):
    """(head, [arm text], tail) of loadBl's switch"""
    s = f.index('\tswitch (type) {\n') + len('\tswitch (type) {\n')
    e = f.index('\n\t}\n', s) + 1
    lines = f[s:e].split('\n')[:-1]
    out, cur = [], None
    prev_case = False
    for l in lines:
        if l.startswith('\tcase ') or l.startswith('\tdefault:'):
            if not prev_case:
                cur = []
                out.append(cur)
            prev_case = True
        else:
            prev_case = False
        cur.append(l)
    return f[:s], ['\n'.join(a) + '\n' for a in out], f[e:]


def names(a):
    return [x.split('\n')[0].strip().split(':')[0].replace('case ', '') for x in a]


def reorder(b, order):
    i, j = bdrun.fnspan(b, LB)
    h, a, t = arms(b[i:j])
    n = names(a)
    a2 = [a[n.index(k)] for k in order]
    return b[:i] + h + ''.join(a2) + t + b[j:]


SRC = None


def CASES(base):
    global SRC
    i, j = bdrun.fnspan(base, LB)
    h, a, t = arms(base[i:j])
    n = names(a)
    assert len(n) == 12, n
    orders = {'src': n}
    for k in range(len(n)):
        for p in range(len(n)):
            if p == k or p == k + 1:
                continue
            o = list(n)
            x = o.pop(k)
            o.insert(p if p < k else p - 1, x)
            orders['mv %s@%d' % (n[k], p)] = o
    num = ['1', '2', '3', '4', '5', '6', '22', '23', '24', '25', '27', 'default']
    orders['numeric'] = num
    orders['rdata'] = ['5', '6', '24', '1', '22', '25', '27', '3', '23', '4', '2', 'default']
    c = []
    for lab, o in orders.items():
        c.append(('on ' + lab, lambda b, o=o: reorder(b, o)))
        c.append(('off ' + lab, lambda b, o=o: off7(reorder(b, o))))
    return c


FOCUS = ['_loadBlFiles']
