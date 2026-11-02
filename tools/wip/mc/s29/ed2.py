"""ed2.py TAG : multi-edit hsim: push subset S of {112,115,103,117,130} in round 3 (rok group) with priority
keys P, optional RX re-keys, f search (fany). Prints minimal sets reaching low inversions."""
import sys, os, random, copy, itertools
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
from evedit import strip
Rr, keys = hsim.load(os.path.join(R, 'build', 'v', 'mc29', 'slot_' + sys.argv[1]))
f0, P0 = hsim.measured(keys)
ROK = hsim.ROK
print('ROK', ROK, 'r3 poppers', list(Rr[2]['g']))
BL = [b for b in [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79] if b in f0]
def pushes(R, S, at):
    R = copy.deepcopy(R)
    for x in S: strip(R, x)
    g = R[2]['g']; g[at] = g.get(at, []) + [('push', x, -1000001) for x in S]
    return R
def fany(Rx, P, restarts=3, BLs=BL):
    random.seed(1); best = (999, None)
    for rs in range(restarts):
        f = dict(f0)
        if rs:
            for b in random.sample(BLs, 4): f[b] = random.randint(0, 8)
        cur = pot.tinv(hsim.sim(Rx, f, P))
        for _ in range(3):
            for b in BLs:
                for v in range(9):
                    g = dict(f); g[b] = v; x = pot.tinv(hsim.sim(Rx, g, P))
                    if x < cur: cur, f = x, g
        if cur < best[0]: best = (cur, {b: f[b] for b in BLs if f[b] != f0[b]})
        if cur == 0: break
    return best
if __name__ == '__main__':
    at = int(sys.argv[2]) if len(sys.argv) > 2 else ROK
    res = []
    C = [112, 115, 103, 117, 130]
    for rx in [(), ('126:125',), ('117:130',), ('126:125', '117:130')]:
        hsim.RXEV.clear()
        for it in rx:
            s, t = map(int, it.split(':')); hsim.RXEV.setdefault(s, []).append(t)
        for n in range(1, 6):
            for S in itertools.combinations(C, n):
                for Pv in itertools.product([1, 3], repeat=n):
                    P = dict(P0); P.update(dict(zip(S, Pv)))
                    if '126:125' in rx: P[125] = P.get(125) or 1
                    if '117:130' in rx: P[130] = P.get(130) or 1
                    r = fany(pushes(Rr, S, at), P, 2)
                    res.append((r[0], rx, S, Pv, r[1])); print(res[-1], flush=True)
                    if r[0] == 0: print('ZERO', res[-1], flush=True)
    res.sort(key=lambda t: t[0]); print('BEST', res[:10])
