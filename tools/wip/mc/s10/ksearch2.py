"""ksearch with realizability: cases freq C<=10 (round 4), HDD<=C/2, erase chain 127,126,125 from case 10.
python ksearch2.py <bbro> iters seed"""
import random, sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\tools\wip'); sys.path.insert(0, ROOT + r'\tools\wip\mc')
import fibsim, fibwhatif, mcsim2
ev = fibsim.parse(sys.argv[1]); R = fibwhatif.groups(ev)
npre = sum(len(r['order']) for r in R[:3])
N = int(sys.argv[2]); random.seed(int(sys.argv[3]))
SEQ = [49, 112, 115, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
CASES = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116, 132]
def ok(x):
    C = x['C']
    if x[112] > C // 2 + (C % 2) or x[115] > C // 2 + (C % 2): return False
    r1 = C - x[127]
    if x[126] > (r1 + 1) // 2: return False
    r2 = r1 - x[126]
    if x[125] > (r2 + 1) // 2: return False
    if x[117] > C or x[130] > C or x[49] > 10: return False
    if not (x[49] >= x[55] >= x[61] >= x[67]): return False
    return True
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
