"""Structured search for FDO frequencies. python mcstage.py <mc bbro> stage1|stage2 ..."""
import os, sys, itertools, json
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip')
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import fibsim, fibwhatif, mcsim2
ev = fibsim.parse(sys.argv[1]); R = fibwhatif.groups(ev)
npre = sum(len(r['order']) for r in R[:3])
WANT = mcsim2.WANT
BIG = [129, 107, 109, 110, 113]
REST = [108, 119, 120, 121, 128, 116, 132]
def run(f):
    try:
        o = mcsim2.sim(R, f)
    except Exception:
        return None
    return [b for b in o[npre:] if b in mcsim2.pos]
def noninc(lo, hi, n):
    return itertools.combinations_with_replacement(range(hi, lo - 1, -1), n)
mode = sys.argv[2]
if mode == 'stage1':
    base = {108: 4, 119: 3, 120: 3, 121: 3, 128: 2, 116: 1, 132: 1, 112: 5, 115: 5, 103: 4, 55: 3, 49: 7, 61: 2, 67: 1, 126: 2, 125: 1, 127: 0, 130: 0, 117: 0, 33: 2, 29: 2, 35: 0, 42: 0, 53: 0, 77: 0, 79: 0}
    n = 0
    for big in noninc(9, 16, 5):
        if sum(big) > 52: continue
        f = dict(base); f.update(zip(BIG, big))
        o = run(f)
        if o and o[:17] == WANT[:17]:
            n += 1; print('OK', big, o[12:20])
    print('stage1 solutions', n)
elif mode == 'stage2':
    big = json.loads(sys.argv[3])
    base = {112: 5, 115: 5, 103: 4, 55: 3, 49: 7, 61: 2, 67: 1, 126: 2, 125: 1, 127: 0, 130: 0, 117: 0, 33: 2, 29: 2, 35: 0, 42: 0, 53: 0, 77: 0, 79: 0}
    base.update(zip(BIG, big))
    n = 0
    for rest in noninc(1, 6, 7):
        if sum(rest) + sum(big) > 67: continue
        f = dict(base); f.update(zip(REST, rest))
        o = run(f)
        if o and o[:17] == WANT[:17]:
            n += 1; print('OK', rest, o[17:])
    print('stage2 solutions', n)
elif mode == 'stage3':
    import random
    design = json.loads(sys.argv[3]); seed = int(sys.argv[4]); iters = int(sys.argv[5])
    random.seed(seed)
    design = {int(k): v for k, v in design.items()}
    B = {61: (0, 3), 67: (0, 3), 73: (0, 2), 81: (0, 1), 126: (0, 2), 125: (0, 2), 127: (0, 1), 130: (0, 1), 117: (0, 1),
         33: (0, 3), 29: (0, 3), 35: (0, 2), 42: (0, 2), 53: (0, 2), 77: (0, 1), 79: (0, 1), 137: (0, 1), 95: (0, 1), 138: (0, 1), 96: (0, 1)}
    cur = dict(design)
    for b, (lo, hi) in B.items(): cur.setdefault(b, 0)
    def sc(f):
        o = run(f)
        if not o or o[:17] != WANT[:17]: return (0, 999)
        return mcsim2.score(o, 0)[:2] if False else (sum(1 for a, b in zip(o, WANT) if a == b), sum(1 for i in range(len(o)) for j in range(i + 1, len(o)) if mcsim2.pos[o[i]] > mcsim2.pos[o[j]]))
    curs = sc(cur); best = (curs, dict(cur)); print('base', curs)
    for it in range(iters):
        f = dict(cur)
        for _ in range(random.randint(1, 3)):
            b = random.choice(list(B)); lo, hi = B[b]; f[b] = max(lo, min(hi, f[b] + random.choice([-1, 1])))
        if not (f[55] >= f[61] >= f[67] >= f[73] >= f[81]): continue
        if f[126] > max(1, (f[121] + 1) // 2) or f[125] > max(1, f[126]) or f[127] > f[121] // 4: continue
        if f[130] > (f[129] + 1) // 2 or f[117] > (f[116] + 1) // 2: continue
        s = sc(f)
        if (-s[1], s[0]) >= (-curs[1], curs[0]) or random.random() < 0.01:
            cur, curs = f, s
            if (-s[1], s[0]) > (-best[0][1], best[0][0]):
                best = (s, dict(f)); print(it, s, {b: v for b, v in sorted(f.items()) if b in B}); print('   ', ' '.join(map(str, run(f))))
                if s[1] == 0: break
    print('best', best)
