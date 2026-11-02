"""fdum.py TAG : hsim what-if combining tail f changes with dummy heap nodes inserted after block X
(fibheap tree-shape lever).  Local search, prints best (inv, fdelta, dummies)."""
import sys, os, random
sys.argv = [sys.argv[0], sys.argv[1]] + sys.argv[2:]
import importlib.util
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
src = open(os.path.join(here, 'dummy.py')).read().split('base = sim(')[0]
g = {'__file__': os.path.join(here, 'dummy.py')}; exec(compile(src, 'dummy', 'exec'), g)
sim, tinv, f0, P0, Rr = g['sim'], g['tinv'], g['f0'], g['P0'], g['Rr']
BL = [b for b in [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79] if b in f0]
base = sim(Rr, f0, P0, None, 0)
def val(f, D):
    X = tuple(d[0] for d in D) if D else None
    # one key for all dummies (sim limitation): use first
    o = sim(Rr, f, P0, X, D[0][1] if D else 0, D[0][2] if D else 1)
    return tinv(o) + 0.3 * sum(abs(f[b] - f0[b]) for b in BL), o
random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
best = (999,)
for rs in range(int(sys.argv[3]) if len(sys.argv) > 3 else 20):
    f = dict(f0); D = []
    if rs:
        D = [(random.choice(base), random.choice([0, -1, -2, -1000101]), random.randint(1, 3))]
    cur, o = val(f, D)
    for it in range(400):
        f2 = dict(f); D2 = list(D)
        r = random.random()
        if r < 0.6:
            b = random.choice(BL); f2[b] = max(0, f2[b] + random.choice([-2, -1, 1, 2]))
        elif r < 0.8:
            D2 = [(random.choice(base), random.choice([0, -1, -2, -3, -1000101]), random.randint(1, 3))]
        else: D2 = []
        x, o2 = val(f2, D2)
        if x <= cur: cur, f, D, o = x, f2, D2, o2
    if cur < best[0]:
        best = (cur, {b: f[b] - f0[b] for b in BL if f[b] != f0[b]}, D, ' '.join(map(str, o[12:])))
        print(best, flush=True)
