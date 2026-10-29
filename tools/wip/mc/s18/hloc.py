"""hloc.py SLOTDIR design.out VARS... : exhaustive over a few f/P variables (b:f:lo-hi, b:P:lo-hi) on a real history."""
import sys, json, itertools, os
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import hsim
R, keys = hsim.load(sys.argv[1])
l = [x for x in open(sys.argv[2]) if x.split(' ')[0].isdigit()][-1]
d = json.loads(l.split(' ', 2)[2])
f0 = {int(k): v for k, v in d['f'].items()}; P0 = {int(k): v for k, v in d['P'].items()}
vs = []
for a in sys.argv[3:]:
    b, kind, r = a.split(':'); lo, hi = map(int, r.split('-'))
    vs.append((int(b), kind, range(lo, hi + 1)))
best = 99
for combo in itertools.product(*[v[2] for v in vs]):
    f, P = dict(f0), dict(P0)
    for (b, kind, _), x in zip(vs, combo):
        (f if kind == 'f' else P)[b] = x
    if any(P.get(b, 0) > f[b] for b in (112, 115, 103)): continue
    if P.get(125): P[125] = (f[126] + 1) // 2
    o = hsim.sim(R, f, P); x = hsim.inv(o)
    if x <= best:
        best = x; print(x, combo, flush=True)
        if x == 0: print(json.dumps({'f': f, 'P': P}))
