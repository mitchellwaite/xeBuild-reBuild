"""Attempt 36: decouple PRE's walk from bbro's tie.  Both follow the 5-test's first edge in if-forms: the loop tree is
rebuilt in RPO (edge order), ch2 creates the arms' preheaders in that order and places each right after the test, so
the true arm gets the higher block index and PRE (dom sons, highest index first) walks it first; bbro's connect_traces
also takes the first edge on a tie.  Here an arm's code goes through a static helper (inlined), so its loops reach the
caller's loop tree through copy_loops, not the RPO rebuild, in case that changes the order.  pin off."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bd470 import arms

FN = 'uint32_t calcBlAreaSize(void)\n'
ded = lambda s: ''.join((l[1:] if l.startswith('\t') else l) for l in s.splitlines(True))


def CASES(base):
    base = bdhints.off(base, 'pin_size')
    i, j, head, J, K, R, tail = arms(base)
    out = []
    # helper bodies: the arm with `return size;` at the end
    def helper(name, body):
        return ('static uint32_t %s(void)\n{\n\tuint32_t size, xs, x;\n\n' % name + ded(body) + '\treturn size;\n}\n\n')
    for which in ('R', 'K', 'RK'):
        for order in ('JKR', 'JRK'):
            pre = ''
            arm = {'J': J, 'K': K, 'R': R}
            if 'R' in which:
                pre += helper('retailAreaSize', R)
                arm['R'] = '\t\tsize = retailAreaSize();\n'
            if 'K' in which:
                pre += helper('kitAreaSize', K)
                arm['K'] = '\t\tsize = kitAreaSize();\n'
            if order == 'JKR':
                s = '\tif (xb.type == BUILD_JTAG) {\n' + arm['J'] + '\t} else if (xb.type > BUILD_DEVGL16) {\n' + arm['K'] + '\t} else {\n' + arm['R'] + '\t}\n'
            else:
                s = '\tif (xb.type == BUILD_JTAG) {\n' + arm['J'] + '\t} else if (xb.type <= BUILD_DEVGL16) {\n' + arm['R'] + '\t} else {\n' + arm['K'] + '\t}\n'
            t = base[:i] + pre + head + s + tail + base[j:]
            out.append(('h%s_%s' % (which, order), t))
    return out
