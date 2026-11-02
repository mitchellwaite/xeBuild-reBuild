# enum4.py DUMP DUMMY : the real dump already has the extra entry DUMMY; enumerate
# 128 source (group/pos), LC114 key override, DUMMY absorber V (visited at V) -> score
import sys, os; sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
pre, g, first = r4sim.load(sys.argv[1]); DM = int(sys.argv[2])
T = list(map(int, os.environ['TT'].split())); OVB = int(os.environ['OVB'])
i = first.index(108); PREF = first[:i+1]
def score(o):
    o = [b for b in o if b != DM]
    return sum(a != b for a, b in zip(o, PREF + [55] + T))
def run(m, V, ov):
    gg = {b: list(v) for b, v in g.items()}
    if m:
        for b in gg: gg[b] = [e for e in gg[b] if not (e[0] == 'ins' and e[2] == 128)]
        L = gg[m[0]]; gg[m[0]] = L[:m[1]] + [('ins', 'this', 128, 0)] + L[m[1]:]
    if V is not None:
        for b in gg: gg[b] = [e for e in gg[b] if e != ('visit', DM)]
        gg[V] = [('visit', DM)] + gg[V]
    try: return r4sim.sim(pre, gg, ov)
    except Exception: return []
res = []
for ovk in (0, -1):
    ov = {OVB: ovk} if ovk else {}
    for m in [None] + [(G, at) for G in first for at in range(len(g[G]) + 1)]:
        for V in [None] + first:
            o = run(m, V, ov); s = score(o)
            res.append((s, ovk, m, V, [b for b in o][17:36]))
res.sort(key=lambda r: r[0])
for r in res[:25]: print(r)
print('no-move best', [r for r in res if r[2] is None][:5])
