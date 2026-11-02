"""tann.py TAG [EVALS] : anneal tail f (0..3) on slot_TAG's real history (hsim); prints best designs.
env FREE=comma blocks (default tail), FMAX."""
import sys, os, random, math, json
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18'))
import hsim
sd = os.path.join(R, 'build', 'v', 'mc27', 'slot_' + sys.argv[1])
EV = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
Rr, keys = hsim.load(sd)
f0, P0 = hsim.measured(keys)
o = hsim.sim(Rr, f0, P0); print('measured', hsim.inv(o), ' '.join(map(str, o)))
FREE = [int(x) for x in os.environ.get('FREE', '126,125,61,33,29,67,127,117,130,35,42,53,77,79,55,112,115,103').split(',')]
FMAX = int(os.environ.get('FMAX', '3'))
random.seed(int(os.environ.get('SEED', '1')))
def cost(f, P):
    c = hsim.inv(hsim.sim(Rr, f, P))
    d = sum(abs(f[b] - f0[b]) for b in FREE) + sum(abs(P.get(b, 0) - P0.get(b, 0)) for b in FREE)
    return c * 10 + d
cur = (dict(f0), dict(P0)); cs = cost(*cur); best = (cs, cur)
for i in range(EV):
    T = 3.0 * (1 - i / EV) + 0.1
    f, P = dict(cur[0]), dict(cur[1])
    b = random.choice(FREE)
    if random.random() < 0.75: f[b] = max(0, min(FMAX, f[b] + random.choice((-1, 1))))
    elif os.environ.get('PRI'): P[b] = max(0, min(FMAX, P.get(b, 0) + random.choice((-1, 1))))
    x = cost(f, P)
    if x <= cs or random.random() < math.exp((cs - x) / T):
        cur, cs = (f, P), x
        if x < best[0]:
            best = (x, cur)
            ch = {b: (cur[0][b], cur[1].get(b, 0)) for b in FREE if cur[0][b] != f0[b] or cur[1].get(b, 0) != P0.get(b, 0)}
            print(i, 'inv', x // 10, 'dist', x % 10 if x < 10 else '', ch, flush=True)
f, P = best[1]
print('best', ' '.join(map(str, hsim.sim(Rr, f, P))))
