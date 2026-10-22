"""Shrink a key-change set that gives the wanted last-round order (wip/fibsolve.py WANT).

python wip/fibmin.py <bbro dump> bb=key ...
Checks the set with wip/fibwhatif.py's replay, then tries every single and pair
removal / +-1 retouch and prints smaller sets that still work.
"""
import sys, itertools
sys.path.insert(0, 'wip')
import fibsim, fibwhatif, fibsolve

ev = fibsim.parse(sys.argv[1]); R = fibwhatif.groups(ev)


def ok(k):
    o = fibwhatif.sim(R, k)
    return [b for b in o[o.index(44):] if b not in fibsolve.FLEX] == fibsolve.WANT


k = dict((int(a), int(b)) for a, b in (x.split('=') for x in sys.argv[2:]))
print('given', ok(k))
changed = True
while changed:
    changed = False
    for b in list(k):
        t = dict(k); del t[b]
        if ok(t):
            print('drop', b, t); k = t; changed = True; break
print('minimal by drops:', len(k), k)
