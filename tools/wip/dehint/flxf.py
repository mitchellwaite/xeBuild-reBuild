"""flxf.py: one and two-axis natural edits at a state with extra tests.  Fixed states below."""
import itertools, random, sys
import fllib as L, flx as X, flx3 as A, flx6 as D, flxe as E

VT = '\t\tlen = memFindChar(&buf[off], 0, sizeof(xb.kernelStr));\n'
STATES = {
 'X0': (('comma', 't'), 'asm', [('off', VT)]),
 'X1': (('comma', 'len'), 'asm', [('off', VT)]),
 'X2': (('comma', 't', 'off3'), 'asm', [('off', VT)]),
}
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 5)
items = [(a, v) for a in A.AXES for v in A.AXES[a]]
V = {}
for st, (dead, fl, ins) in STATES.items():
    combos = [()] + [(x,) for x in items] + [c for c in itertools.combinations(items, 2) if c[0][0] != c[1][0]]
    rng.shuffle(combos)
    combos = sorted(combos[:N], key=len)
    for c in combos:
        ch = dict(c)
        try:
            s = E.put(A.apply(X.gen(dead, fl), ch), ins)
        except ValueError:
            continue
        V[st + ':' + ','.join('%s=%s' % kv for kv in sorted(ch.items()))] = s
print(len(V))
rs = L.sweep(V, prefix='f', show=30)
from collections import Counter
print(sorted(Counter((n.split(':')[0], r[0]) for n, r in rs).items(), key=lambda x: x[0][1])[:15])
X.write(rs, 'xf.txt')
