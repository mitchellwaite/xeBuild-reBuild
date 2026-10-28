"""random/hill-climb over cold-block frequencies (0..MAX) on a bbro history with mcsim2.
python ksearch.py <mode_client bbro> [iters] [max]"""
import random, sys, time
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\wip'); sys.path.insert(0, ROOT + r'\wip\mc')
import fibsim, fibwhatif, mcsim2
ev = fibsim.parse(sys.argv[1]); R = fibwhatif.groups(ev)
npre = sum(len(r['order']) for r in R[:3])
N = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
MX = int(sys.argv[3]) if len(sys.argv) > 3 else 10
SEQ = [49, 112, 115, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
def score(f):
    try: o = mcsim2.sim(R, f)
    except Exception: return 999, 0, None
    pre, inv, oo = mcsim2.score(o, npre)
    return inv, pre, oo
t = time.time(); base = {b: 0 for b in SEQ}
print('identity', score({})[:2], time.time() - t)
random.seed(int(sys.argv[4]) if len(sys.argv) > 4 else 1)
best = None; bs = (999,)
for it in range(N):
    if best is None or random.random() < 0.05:
        vals = sorted((random.randint(0, MX) for _ in SEQ), reverse=True)
        x = dict(zip(SEQ, vals))
    else:
        x = dict(best)
        for _ in range(random.choice((1, 1, 2))):
            b = random.choice(SEQ); x[b] = min(MX, max(0, x[b] + random.choice((-1, 1))))
    inv, pre, oo = score(x)
    s = (inv, -pre)
    if s <= bs:
        if s < bs: print(it, inv, pre, x, flush=True)
        bs, best = s, x
        if inv == 0: print('PERFECT', x, ' '.join(map(str, oo))); break
print('best', bs, best)
