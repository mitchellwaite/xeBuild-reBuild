"""fanneal.py SLOT EVALS SEED : f-only anneal on the plain history (P as measured, f 0..FMAX, no FDO constraints).
Answers: does any frequency assignment on the plain compile's insertion history reach inv 0?"""
import sys, json, random, math, os
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import hsim
sd, EV, SEED = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
random.seed(SEED)
R, keys = hsim.load(sd)
f0, P0 = hsim.measured(keys)
f0.update(hsim.armf(sd))
FMAX = int(os.environ.get('FMAX', '10'))
PTIE = os.environ.get('PTIE')  # P follows f for blocks whose measured P==f
tie = {b for b in f0 if P0.get(b) == f0[b] and f0[b] > 0} if PTIE else set()
FK = sorted(f0)
def val(f):
    P = dict(P0)
    for b in tie: P[b] = f[b]
    return 100 * hsim.inv(hsim.sim(R, f, P)) + (sum(abs(f[b] - f0[b]) for b in f) if os.environ.get("DIST") else 0)
cur = dict(f0)
if os.environ.get("START"): cur.update({int(k): v for k, v in json.load(open(os.environ["START"])).items()})
cs = val(cur); best, bs = cur, cs
print('start', cs, flush=True)
for i in range(EV):
    T = float(os.environ.get("T0", "1")) * (1 - i / EV) + 0.05
    f = dict(cur)
    for _ in range(random.choice((1, 1, 2, 3))):
        b = random.choice(FK); f[b] = max(0, min(FMAX, f[b] + random.choice((-1, 1))))
    x = val(f)
    if x <= cs or random.random() < math.exp((cs - x) / T):
        cur, cs = f, x
        if x < bs:
            best, bs = f, x
            print(i, bs, json.dumps(best), flush=True)
            if bs == 0 and not os.environ.get("DIST"): break
print('best', bs, json.dumps(best))
