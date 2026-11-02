"""ed3.py TAG : push subset S (round 3, at rok) with priority keys, 49's key made priority, and
coordinate descent over f (0..8) AND P (0..9) of S+49 (+125/130 RX re-keys). Model of the s18 match."""
import sys, os, random, copy, itertools
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
from evedit import strip
Rr, keys = hsim.load(os.path.join(R, 'build', 'v', 'mc29', 'slot_' + sys.argv[1]))
f0, P0 = hsim.measured(keys)
BL = [b for b in [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79] if b in f0]
def edit(R, S, at=1102, p49=True):
    R = copy.deepcopy(R)
    for x in S: strip(R, x)
    g = R[2]['g']; g[at] = g.get(at, []) + [('push', x, -1000001) for x in S]
    if p49:
        for b, es in g.items():
            g[b] = [('ins', e[1], 49, -1000001) if e[0] == 'ins' and e[2] == 49 else e for e in es]
    return R
def search(Rx, PB, restarts=3, seed=1):
    random.seed(seed); best = (999, None, None)
    for rs in range(restarts):
        f = dict(f0); P = dict(P0)
        for b in PB: P[b] = P.get(b) or 1
        if rs:
            for b in random.sample(BL, 4): f[b] = random.randint(0, 8)
            for b in PB: P[b] = random.randint(1, 6)
        sc = lambda f, P: pot.tinv(hsim.sim(Rx, f, P))
        cur = sc(f, P)
        for _ in range(4):
            ch = False
            for b in BL:
                for v in range(9):
                    g = dict(f); g[b] = v; x = sc(g, P)
                    if x < cur: cur, f, ch = x, g, True
            for b in PB:
                for v in range(0, 10):
                    Q = dict(P); Q[b] = v; x = sc(f, Q)
                    if x < cur: cur, P, ch = x, Q, True
            if not ch: break
        if cur < best[0]: best = (cur, {b: f[b] for b in BL if f[b] != f0[b]}, {b: P[b] for b in PB})
        if cur == 0: break
    return best
if __name__ == '__main__':
    C = [112, 115, 103, 117, 130]
    res = []
    for rx in [('126:125', '117:130'), ()]:
        hsim.RXEV.clear()
        for it in rx:
            s, t = map(int, it.split(':')); hsim.RXEV.setdefault(s, []).append(t)
        for n in range(0, 6):
            for S in itertools.combinations(C, n):
                PB = list(S) + [49] + ([125, 130] if rx else [])
                r = search(edit(Rr, S), PB, 3)
                res.append((r[0], rx, S, r[1], r[2])); print(res[-1], flush=True)
    res.sort(key=lambda t: t[0]); print('BEST', res[:10])
