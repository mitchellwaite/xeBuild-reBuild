# enum1.py DUMP : dummy D inserted by group G at pos/key, absorbed (visited) by group V; score vs target
import sys; sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
pre, g, first = r4sim.load(sys.argv[1])
T = list(map(int, "144 143 62 33 29 69 146 128 149 35 42 53 79 81".split()))
i = first.index(108); PREF = first[:i+1]; D = 9999
def score(o):
    o = [b for b in o if b < D]
    return sum(a != b for a, b in zip(o, PREF + [55] + T)) + abs(len(o) - len(first))
def run(G, at, k, V, gv_at=0):
    gg = {b: list(v) for b, v in g.items()}
    L = gg[G]; gg[G] = L[:at] + [('ins', 'this', D, k)] + L[at:]
    if V is not None: L = gg[V]; gg[V] = L[:gv_at] + [('visit', D)] + L[gv_at:]
    try: return r4sim.sim(pre, gg, {})
    except Exception as e: return []
print('base', score(r4sim.sim(pre, g, {})))
res = []
for G in first:
  for at in range(len(g[G]) + 1):
    for k in (-2, -1, 0):
      for V in [None] + first:
        if V == G: continue
        o = run(G, at, k, V); s = score(o)
        res.append((s, G, at, k, V, [b for b in o if b != D][18:34] , D in o and o.index(D)))
res.sort(key=lambda r: r[0])
for r in res[:40]: print(r)
