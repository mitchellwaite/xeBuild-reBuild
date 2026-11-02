# enum2.py DUMP : (146 key, 128 source group/pos) x dummy (G,at,k,V absorber or None)
import sys; sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
pre, g, first = r4sim.load(sys.argv[1])
import os; T = list(map(int, os.environ.get("TT", "144 143 62 33 29 69 146 128 149 35 42 53 79 81").split())); OVB = int(os.environ.get("OVB", "146"))
i = first.index(108); PREF = first[:i+1]; D = 9999
def score(o):
    o = [b for b in o if b < D]
    return sum(a != b for a, b in zip(o, PREF + [55] + T)) + abs(len(o) - len(first))
def mv(gg, blk, to, at):
    for b in gg: gg[b] = [e for e in gg[b] if not (e[0] == 'ins' and e[2] == blk)]
    L = gg[to]; gg[to] = L[:at] + [('ins', 'this', blk, 0)] + L[at:]
def run(m128, dm, ov):
    gg = {b: list(v) for b, v in g.items()}
    if m128: mv(gg, 128, *m128)
    if dm:
        G, at, k, V = dm; L = gg[G]; gg[G] = L[:at] + [('ins', 'this', D, k)] + L[at:]
        if V is not None: gg[V] = [('visit', D)] + gg[V]
    try: return r4sim.sim(pre, gg, ov)
    except Exception: return []
M = [None] + [(G, at) for G in (108, 121) for at in range(len(g[G]) + 1)]
DM = [None] + [(G, at, k, V) for G in first for at in range(len(g[G]) + 1) for k in (-2, -1, 0) for V in [None] + first if V != G]
best = []
for ovk in (0, -1):
  ov = {OVB: ovk} if ovk else {}
  for m in M:
    s0 = score(run(m, None, ov))
    if s0 > 8: continue
    for dm in DM:
      o = run(m, dm, ov); s = score(o)
      if s <= 2: print(s, ovk, m, dm, [b for b in o if b < D][18:34], flush=True)
