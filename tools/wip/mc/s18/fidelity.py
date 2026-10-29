"""fidelity.py SLOTDIR : feed the real measured keys of a compile into fake7's sim; compare orders."""
import os, sys, json
sd = sys.argv[1]
sys.argv = ['x', '0', '1']
import fake7, analyze
order, inv, keys, named = analyze.analyze(sd)
f, P = {}, {}
for b, (p, v) in keys.items():
    if isinstance(b, str):
        if b == 'k94': f[94] = v
        continue
    f[b] = v if v is not None and v >= 0 else 0
    if p: P[b] = p
for b in fake7.FK:
    if b not in f: f[b] = named['fq'].get(b, 0) or 0
P.setdefault(132, 0)
for c in fake7.CASES: P.setdefault(c, 0)
P['d49'] = P.get(49, f[49]) - f[49]
P['x126_125'] = P.get(125, 0); P['x117_130'] = P.get(130, 0)
fake7.X1ORD = [int(x) for x in os.environ.get('X1ORD', '112,115,121').split(',')]
PP = dict(P)
print('ok', fake7.ok(f, PP))
o = fake7.sim(f, PP)
print('real', ' '.join(str(b) for b in order if b in fake7.mcsim2.pos), 'inv', inv)
print('sim ', ' '.join(map(str, o)), 'inv', fake7.inv(o))
