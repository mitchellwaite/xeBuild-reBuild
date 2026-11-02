# enum3.py DUMP : 128 stays in its group; 146 key in {0,-1}; up to two dummies (G,at,k) (unabsorbed or absorbed)
import sys, itertools; sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
exec(open('enum2.py').read().split('M = [None]')[0].split('pre, g, first')[1].join(['pre, g, first','']) if False else '')
pre, g, first = r4sim.load(sys.argv[1])
import os; T = list(map(int, os.environ.get("TT", "144 143 62 33 29 69 146 128 149 35 42 53 79 81").split())); OVB = int(os.environ.get("OVB", "146"))
i = first.index(108); PREF = first[:i+1]; D = 9999
def score(o):
    o = [b for b in o if b < D]
    return sum(a != b for a, b in zip(o, PREF + [55] + T)) + abs(len(o) - len(first))
def run(dms, ov):
    gg = {b: list(v) for b, v in g.items()}
    for n, (G, at, k, V) in enumerate(dms):
        L = gg[G]; gg[G] = L[:at] + [('ins', 'this', D + n, k)] + L[at:]
        if V is not None: gg[V] = [('visit', D + n)] + gg[V]
    try: return r4sim.sim(pre, gg, ov)
    except Exception: return []
DM = [(G, at, k, None) for G in first[:30] for at in range(len(g[G]) + 1) for k in (-2, -1, 0)]
res = []
for ovk in (0, -1):
    ov = {OVB: ovk} if ovk else {}
    for a in DM:
        res.append((score(run([a], ov)), ovk, [a]))
    for a, b in itertools.combinations(DM, 2):
        res.append((score(run([a, b], ov)), ovk, [a, b]))
res.sort(key=lambda r: r[0])
for r in res[:15]: print(r, [x for x in run(r[2], {OVB: r[1]} if r[1] else {}) if x < D][17:34])
