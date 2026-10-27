"""Search FDO-realizable frequencies: switch cases (sum <= SUM), HDD errors = half of case 4/5, others bounded.
python mcfsearch.py <mc bbro> seed iters [SUM]"""
import os, sys, random
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\wip')
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import fibsim, fibwhatif, mcsim2
ev = fibsim.parse(sys.argv[1]); R = fibwhatif.groups(ev)
npre = sum(len(r['order']) for r in R[:3])
random.seed(int(sys.argv[2])); iters = int(sys.argv[3]); SUM = int(sys.argv[4]) if len(sys.argv) > 4 else 66
CASES = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116, 132]
FREE = {112: (0, 8), 115: (0, 8), 103: (4, 4), 55: (1, 3), 61: (0, 2), 67: (0, 1), 126: (0, 2), 125: (0, 2), 127: (0, 1), 130: (0, 2), 117: (0, 2), 33: (0, 2), 29: (0, 2), 35: (0, 1), 42: (0, 1), 53: (0, 1), 77: (0, 1), 79: (0, 1), 49: (5, 9)}
def derive(f):
    g = dict(f)
    return g
def evaluate(f):
    try:
        o = mcsim2.sim(R, derive(f))
    except Exception:
        return (0, 999, [])
    return mcsim2.score(o, npre)
cur = {129: 11, 107: 11, 109: 11, 110: 10, 113: 10, 108: 3, 119: 2, 120: 2, 121: 3, 128: 2, 116: 1, 132: 1, 112: 5, 115: 5, 103: 4, 55: 3, 61: 2, 67: 1, 126: 2, 125: 1, 127: 0, 130: 0, 117: 0, 33: 2, 29: 2, 35: 0, 42: 0, 53: 0, 77: 0, 79: 0, 49: 7}
curs = evaluate(cur); best = (curs[:2], dict(cur))
print('base', curs[:2])
for it in range(iters):
    f = dict(cur)
    for _ in range(random.randint(1, 3)):
        if random.random() < 0.6:
            b = random.choice(CASES); f[b] = max(1, min(16, f[b] + random.choice([-3, -2, -1, 1, 2, 3])))
        else:
            b = random.choice(list(FREE)); lo, hi = FREE[b]; f[b] = max(lo, min(hi, f[b] + random.choice([-1, 1])))
    if sum(f[c] for c in CASES) > SUM: continue
    if not (f[49] >= f[55] >= f[61] >= f[67]): continue
    if f[112] > (f[110] + 1) // 2 or f[115] > (f[113] + 1) // 2: continue
    if f[126] > max(1, (f[121] + 1) // 2) or f[125] > max(1, f[126]) or f[127] > max(0, f[121] // 4): continue
    if f[130] > (f[129] + 1) // 2 or f[117] > (f[116] + 1) // 2: continue
    s = evaluate(f)
    if (-s[1], s[0]) >= (-curs[1], curs[0]) or random.random() < 0.01:
        cur, curs = f, s
        if (-s[1], s[0]) > (-best[0][1], best[0][0]):
            best = (s[:2], dict(f)); print(it, s[:2], {b: v for b, v in sorted(f.items())}); print('   ', ' '.join(map(str, s[2])))
            if s[1] == 0: break
print('best', best)
