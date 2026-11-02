# shape.py DUMP : r4sim structural search (heap SHAPE edits, not keys) for the reference tail.
# edits: D(pos,key) dummy push at pre position pos (rounds 2-3) [optionally deleted when block X pops in r4];
#        R(pos) drop a push/ins-next at pos; S(pos) swap push pos with next push; G(b,key) dummy insert in r4 group of b.
import sys, itertools, copy
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
pre, g, first = r4sim.load(sys.argv[1])
T = list(map(int, "62 33 29 69 146 128 151 35 42 53 79 81".split()))
i143 = first.index(143); PREF = first[:i143+1]
DUM = 9999
def score(o):
    o = [b for b in o if b < DUM]
    s = sum(a != b for a, b in zip(o[:i143+1], PREF))
    if 143 not in o: return 99
    j = o.index(143); t = o[j+1:j+1+len(T)]
    return s + sum(a != b for a, b in zip(t, T))
def run(p, gg):
    try: return r4sim.sim(p, gg, {})
    except Exception as ex: return []
base = run(pre, g); print('base', score(base))
r3 = [i for i, e in enumerate(pre) if e[0] == 'round'][1]
pp = [i for i, e in enumerate(pre) if i > r3 and (e[0] == 'push' or (e[0] == 'ins' and e[1] == 'next'))]
keys = [-1000406, -1000306, -1000204, -1000104, -8, -7, -4, -3, -2, -1, 0, 1]
res = []
def rec(name, p, gg):
    o = run(p, gg); res.append((score(o), name, [b for b in o if b < DUM][i143+1:i143+16]))
# dummies in round 2-3 (push into next heap)
for pos in range(r3 - 0, len(pre) + 1):
    for k in keys:
        p = pre[:pos] + [('push', DUM, k)] + pre[pos:]; rec(('D', pos, k), p, g)
        # deleted (visited) when some r4 block pops
        for x in [143, 62, 33, 29, 69, 55, 108, 144]:
            gg = dict(g); gg[x] = [('visit', DUM)] + g[x]; rec(('Dv', pos, k, x), p, gg)
for pos in pp:
    p = pre[:pos] + pre[pos+1:]; rec(('R', pos, pre[pos]), p, g)
for a, b in zip(pp, pp[1:]):
    p = list(pre); p[a], p[b] = p[b], p[a]; rec(('S', a, b), p, g)
for b in first[i143-8:]:
    for k in keys:
        for at in range(len(g.get(b, [])) + 1):
            gg = dict(g); gg[b] = g[b][:at] + [('ins', 'this', DUM, k)] + g[b][at:]; rec(('G', b, at, k), pre, gg)
res.sort(key=lambda r: r[0])
for r in res[:25]: print(r)
