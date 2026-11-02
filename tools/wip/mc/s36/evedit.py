"""evedit.py TAG : hsim with EVENT edits on TAG's history + fany-style f search.
Edits tried: move block X's round-4 insertion to a round-3 push (after group G), drop/move inserts."""
import sys, os, random, copy, itertools
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
Rr, keys = hsim.load(os.path.join(R, 'build', 'v', 'mc36', 'slot_' + sys.argv[1]))
f0, P0 = hsim.measured(keys)
BL = [b for b in [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79] if b in f0]

def strip(R, x):
    for r in R[3:]:
        for b, es in r['g'].items():
            r['g'][b] = [e for e in es if not (e[0] == 'ins' and e[2] == x)]
def to_push(R, x, after):          # x becomes a round-3 push (round-4 heap at start)
    R = copy.deepcopy(R); strip(R, x)
    g = R[2]['g']; g.setdefault(after, []); g[after] = g[after] + [('push', x, -1)]
    return R
def move_ins(R, x, popper):        # x inserted ('this') while popper is visited in round 4
    R = copy.deepcopy(R); strip(R, x)
    g = R[3]['g']; g[popper] = g.get(popper, []) + [('ins', 'this', x, -1)]
    return R
def fany(Rx, restarts=8, P=None):
    P = P or P0; random.seed(1); best = (999, None)
    for rs in range(restarts):
        f = dict(f0)
        if rs:
            for b in random.sample(BL, 4): f[b] = random.randint(0, 8)
        try: cur = pot.tinv(hsim.sim(Rx, f, P))
        except Exception: return (999, None)
        for _ in range(3):
            for b in BL:
                for v in range(9):
                    g = dict(f); g[b] = v; x = pot.tinv(hsim.sim(Rx, g, P))
                    if x < cur: cur, f = x, g
        if cur < best[0]: best = (cur, {b: f[b] for b in BL if f[b] != f0[b]})
        if cur == 0: break
    return best
if __name__ == '__main__':
    print('base', fany(Rr, 4), flush=True)
    r3 = [b for b in Rr[2]['g']]
    pop4 = [b for b in Rr[3]['g']]
    res = []
    for x in [112, 115, 126, 77, 79, 53, 55, 61, 125]:
        for a in r3:
            res.append((fany(to_push(Rr, x, a), 3), 'push', x, a)); print(res[-1], flush=True)
        for p in pop4:
            res.append((fany(move_ins(Rr, x, p), 3), 'ins', x, p)); print(res[-1], flush=True)
    res.sort(key=lambda t: t[0][0]); print('BEST', res[:15])
