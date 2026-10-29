"""Exhaustive nonincreasing tail-frequency enumeration on top of a prefix design (fake7 sim).
python tailenum.py best.out [maxlevel]   env as fake7 (RX, TX2, X1, X2CASES ...)"""
import os, sys, json, itertools, time
src, ML = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 3
sys.argv = ['x', '0', '1']
import fake7
l = [x for x in open(src) if x.startswith('best')][0]
d = json.loads(l.split(' ', 2)[2])
f0 = {int(k): v for k, v in d['f'].items()}
P0 = {(int(k) if k.lstrip('-').isdigit() else k): v for k, v in d['P'].items()}
TAIL = [55, 126, 61, 33, 29, 67, 127, 117, 35, 42, 53, 77, 79]
res = {}
best = (99, None)
n = 0; t0 = time.time()
for comb in itertools.combinations_with_replacement(range(ML, -1, -1), len(TAIL)):
  for v125 in range(ML + 1):
   for v130 in range(ML + 1):
    for xr, xq in ((0, 0), (1, 0), (0, 1), (1, 1)):
        f = dict(f0); P = dict(P0)
        for b, v in zip(TAIL, comb): f[b] = v
        f[125] = v125; f[130] = v130
        P['x126_125'] = xr
        P['x117_130'] = xq
        PP = dict(P)
        if not fake7.ok(f, PP): continue
        n += 1
        x = fake7.inv(fake7.sim(f, PP))
        if x < best[0]:
            best = (x, (comb, v125, v130, xr, xq)); print(x, comb, v125, v130, xr, xq, flush=True)
        if x == 0:
            print('ZERO', json.dumps({'f': f, 'P': P}), flush=True)
print('done', n, time.time() - t0, best)
