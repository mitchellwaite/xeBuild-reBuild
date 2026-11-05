"""Attempt 17: costs on the attempt 17 draft: attribute subsets x pin forms."""
import os, sys, itertools, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ir17lib, irlib
from ir17lib import score, diff
P = os.path.join(irlib.R, 'tools', 'wip', 'dehint', 'drafts', 'image_read_attempt17.c')
D = open(P, newline='').read()
ATT = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc'
PIN = '__asm__("" : "+D"(addr));'
AT = {'a3': ('no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'), 'i2tm': ('no-if-conversion2', 'no-tree-tail-merge'), 'i1tm': ('no-if-conversion', 'no-tree-tail-merge'), 'i1i2': ('no-if-conversion', 'no-if-conversion2'),
      'tm': ('no-tree-tail-merge',), 'i2': ('no-if-conversion2',), 'i1': ('no-if-conversion',), 'a0': ()}
PINS = {'pin': PIN, 'asm0': '__asm__("");', 'empty': ';'}
def var(a, p):
    at = AT[a]
    s = ('__attribute__((optimize(' + ', '.join('"%s"' % x for x in at) + '))) ' if at else '') + 'void getImageSmc'
    return D.replace(ATT, s).replace(PIN, PINS[p])
if __name__ == '__main__':
    res = []
    for a, p in itertools.product(AT, PINS):
        s = score(var(a, p))
        res.append((s[1], s[0], a, p, s[2], s[3]))
    for r in sorted(res, key=lambda x: (x[0], x[1])):
        print(r)
