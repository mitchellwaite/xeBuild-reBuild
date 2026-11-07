"""Attempt 57: loadBlFiles' case order in the loop form (attempt 30 swept it on the old helper form
only): each case block moved to every other place in the switch, scored with each loader hint off
(pr, bar, lab) and none off.  Same for loadConsoleBlFiles with lab_none off (A57_CON=1).
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a57_corder.py"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a57lib import *

FN = 'int loadConsoleBlFiles(void)\n{' if os.environ.get('A57_CON') else 'int loadBlFiles(void)\n{'


def blocks(t):
    i = t.index(FN)
    a = t.index('\t\t\tswitch (type) {\n', i) + len('\t\t\tswitch (type) {\n')
    b = t.index('\t\t\t}\n\t\t}\n\t\tif (r) {', a)
    body = t[a:b]
    lines = body.splitlines(True)
    bl = []
    for l in lines:
        if re.match(r'^\t\t\t(case |default:)', l) and (not bl or not re.match(r'^\t\t\t(case |default:)', bl[-1][-1])):
            bl.append([l])
        else:
            bl[-1].append(l)
    return t[:a], [''.join(x) for x in bl], t[b:]


def mv(src, dst):
    def f(t):
        h, bl, tl = blocks(t)
        x = bl.pop(src)
        bl.insert(dst, x)
        return h + ''.join(bl) + tl
    return f


def comp(f, ed):
    return lambda t: H_apply(f(t), ed)


t0 = open(BASE, newline='').read()
_, BL, _ = blocks(t0)
n = len(BL)
offs = ('', 'none') if os.environ.get('A57_CON') else ('', 'pr', 'bar', 'lab')
V = {}
for s in range(n):
    for d in range(n):
        if s == d:
            continue
        for k in offs:
            V['m%d_%d%s' % (s, d, '_' + k if k else '')] = comp(mv(s, d), OFFS[k])
