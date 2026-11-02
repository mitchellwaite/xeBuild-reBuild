import sys, time
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s104')
from srch import *
pre, g, first = r4sim.load(sys.argv[1]); W = int(sys.argv[2]); DEP = int(sys.argv[3])
blocks = sorted(set(first) | {141, 139, 145, 138, 140, 127, 55, 108})
keys = list(range(-10, 2))
r3 = pre.index(('round', 3)); pts = [('p', i + 1) for i in range(r3, len(pre)) if pre[i][0] == 'visit'] + [(b, j) for b in g for j in range(len(g[b]) + 1)]
edits = [('ov', b, k) for b in blocks for k in keys] + [('dum', p, k) for p in pts for k in (-8, -5, -4, -3, -2, -1, 0, 1)]
def run(es):
    ov = {}; du = {}
    for t, a, k in es: (ov if t == 'ov' else du)[a] = k
    return sim(pre, g, ov, du)
print(len(edits), 'edits'); t0 = time.time()
beam = [(dist(first), ())]; seen = set()
for d in range(DEP):
    cand = []
    for sc, es in beam:
        used = {a for _, a, _ in es}
        for e in edits:
            if e[1] in used: continue
            ne = tuple(sorted(es + (e,), key=str))
            if ne in seen: continue
            seen.add(ne); o = run(ne); cand.append((dist(o), ne))
            if o == T: print('HIT', ne); sys.stdout.flush()
    cand.sort(key=lambda r: r[0])
    # diversify: keep at most W, prefer distinct
    beam = cand[:W]
    print('depth', d + 1, 'best', beam[0][0], beam[0][1], round(time.time() - t0)); sys.stdout.flush()
    hits = [c for c in cand if c[0] == 0]
    if hits:
        for h in hits[:40]: print('ZERO', h[1])
        break
