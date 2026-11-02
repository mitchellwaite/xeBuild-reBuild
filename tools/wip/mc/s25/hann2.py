"""hann2.py TAG EVALS SEED : anneal f/P of all non-loop round-4 blocks (cases + tail) on the real
history of slot_TAG (s18 hsim), objective = true inversions (ev.WANT) + 5*missing + small L1 distance.
Loop blocks (55 61 33 29 67 35 42 53 77 79 ...) keep their measured keys.  Prints improving designs."""
import sys, os, random, math, json
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, ev
sd = os.path.join(R, 'build', 'v', 'mc25', 'slot_' + sys.argv[1])
EV, SEED = int(sys.argv[2]), int(sys.argv[3])
random.seed(SEED)
Rr, keys = hsim.load(sd)
f0, P0 = hsim.measured(keys)
CASES = ev.CASES
TAIL = [115, 112, 103, 126, 125, 127, 117, 130]
FREE = [b for b in CASES + TAIL if b in f0]
if os.environ.get('ONLY'): FREE = [int(x) for x in os.environ['ONLY'].split(',')]
W = float(os.environ.get('W', '0.2'))


def tinv(o):
    inv, miss, oo = ev.score_order([str(b) for b in o])
    return inv + 5 * len(miss)


def cost(f, P):
    o = hsim.sim(Rr, f, P)
    d = sum(abs(f[b] - f0[b]) + abs(P.get(b, 0) - P0.get(b, 0)) for b in FREE)
    return tinv(o) + W * d, o


cur = (dict(f0), dict(P0)); cs, o = cost(*cur); best = cs
print('measured', cs, ' '.join(map(str, o)), flush=True)
T0 = float(os.environ.get('T0', '2'))
for i in range(EV):
    T = T0 * (1 - i / EV) + 0.05
    f, P = dict(cur[0]), dict(cur[1])
    for _ in range(random.choice((1, 1, 2))):
        b = random.choice(FREE)
        if random.random() < 0.6: f[b] = max(0, min(8, f[b] + random.choice((-1, 1))))
        else: P[b] = max(0, min(8, P.get(b, 0) + random.choice((-1, 1))))
    x, o = cost(f, P)
    if x <= cs or random.random() < math.exp((cs - x) / T):
        cur, cs = (f, P), x
        if x < best:
            best = x
            ch = {b: '%d/%d' % (f[b], P.get(b, 0)) for b in FREE if f[b] != f0[b] or P.get(b, 0) != P0.get(b, 0)}
            print(i, round(x, 2), tinv(o), json.dumps(ch), ' '.join(map(str, o[11:])), flush=True)
