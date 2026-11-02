"""fanneal2.py SLOT TABLE EVALS SEED: s20 fanneal restricted to blocks some measured single injection
(TABLE rows without missing blocks) moves, plus flow rules: 112 <= f110/2, 115 <= f113/2 (the HDD log
must not beat the send call or trace growth claims it), f >= 0. Objective 100*inv + L1 from base."""
import sys, json, random, math, os
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import hsim
sd, tab, EV, SEED = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
random.seed(SEED)
R, keys = hsim.load(sd)
f0, P0 = hsim.measured(keys); f0.update(hsim.armf(sd))
T = json.load(open(tab))
MOV = sorted({int(k) for r in T['rows'] if not r['miss'] for k in r['d']} & set(f0))
MOV = sorted(set(MOV if not os.environ.get('ONLY') else []) | {int(x) for x in os.environ.get('EXTRA', '').split(',') if x})
print('movable', MOV)
tie = {b for b in f0 if P0.get(b) == f0[b] and f0[b] > 0}
FMAX = int(os.environ.get('FMAX', '12'))
def flow(f):
    pen = 0
    if 110 in f and 112 in f: pen += max(0, f[112] - f[110] // 2)
    if 113 in f and 115 in f: pen += max(0, f[115] - f[113] // 2)
    return pen
def val(f):
    P = dict(P0)
    for b in tie: P[b] = f[b]
    return 100 * hsim.inv(hsim.sim(R, f, P)) + 300 * flow(f) + sum(abs(f[b] - f0[b]) for b in f)
cur = dict(f0); cs = val(cur); best, bs = cur, cs
print('start', cs, flush=True)
for i in range(EV):
    t = float(os.environ.get('T0', '30')) * (1 - i / EV) + 0.5
    f = dict(cur)
    for _ in range(random.choice((1, 1, 2, 3))):
        b = random.choice(MOV); f[b] = max(0, min(FMAX, f[b] + random.choice((-1, 1))))
    x = val(f)
    if x <= cs or random.random() < math.exp((cs - x) / t):
        cur, cs = f, x
        if x < bs: best, bs = f, x; print(i, bs, flush=True)
print('best', bs, json.dumps({b: best[b] for b in best if best[b] != f0[b]}))
P = dict(P0)
for b in tie: P[b] = best[b]
print('inv', hsim.inv(hsim.sim(R, best, P)), 'flow', flow(best))
