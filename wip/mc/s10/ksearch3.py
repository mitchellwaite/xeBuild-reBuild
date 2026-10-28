"""ksearch with realizability: cases freq C<=10 (round 4), HDD<=C/2, erase chain 127,126,125 from case 10.
python ksearch2.py <bbro> iters seed"""
import random, sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\wip'); sys.path.insert(0, ROOT + r'\wip\mc')
import fibsim, fibwhatif, mcsim2
ev = fibsim.parse(sys.argv[1]); R = fibwhatif.groups(ev)
npre = sum(len(r['order']) for r in R[:3])
N = int(sys.argv[2]); random.seed(int(sys.argv[3]))
SEQ = [49, 112, 115, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
CASES = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116, 132]
C9 = float(__import__('os').environ.get('CMAX', '9.49'))
lo = lambda t: max(0.0, t - 0.5)
def ok(x):
    C = C9
    if lo(x[112]) > C / 2 or lo(x[115]) > C / 2: return False
    a = lo(x[127]); b = lo(x[126]); c = lo(x[125])
    if b > (C - a) / 2 + 1e-9: return False
    if c > (C - a - b) / 2 + 1e-9: return False
    if x[49] > 9 or x[117] > 9 or x[130] > 9: return False
    return x[49] >= x[55] >= x[61] >= x[67]
def score(x):
    f = {b: x[b] for b in SEQ}
    pass
    try: o = mcsim2.sim(R, f)
    except Exception: return 999, 0, None
    pre, inv, oo = mcsim2.score(o, npre)
    return inv, pre, oo
best = None; bs = (999,)
for it in range(N):
    if best is None or random.random() < 0.03:
        x = {b: random.randint(0, 10) for b in SEQ}; x['C'] = random.randint(7, 10)
    else:
        x = dict(best)
        for _ in range(random.choice((1, 1, 2, 3))):
            b = random.choice(SEQ + ['C']); x[b] = min(10, max(0, x[b] + random.choice((-1, 1))))
    if not ok(x): continue
    inv, pre, oo = score(x)
    s = (inv, -pre)
    if s <= bs:
        if s < bs: print(it, inv, pre, x, flush=True)
        bs, best = s, x
        if inv == 0: print('PERFECT', x, ' '.join(map(str, oo))); break
print('best', bs, best)
