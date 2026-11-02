"""ed4.py : start from the s18 MATCH history, revert subsets of its features to the g7b form, f search.
Features: A 112 r3-prio push, B 115, C 103 prio, D 117 at rok, E 130 at rok, F 125 rekey@126, G 130 rekey@117, H 49 prio."""
import sys, os, random, copy, itertools
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
def strip(R, x):
    for r in R[3:]:
        for b, es in r['g'].items():
            r['g'][b] = [e for e in es if not (e[0] == 'ins' and e[2] == x)]
    for r in R[2:3]:
        for b, es in r['g'].items():
            r['g'][b] = [e for e in es if not (e[0] == 'ins' and e[2] == x)]
Rm, keys = hsim.load(os.path.join(R, 'build', 'v', 'mc29', 'slot_match'))
f0, P0 = hsim.measured(keys)
BL = [b for b in [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79] if b in f0]
POP = {112: 110, 115: 109, 117: 116, 130: 129}
def revert(R, feats):
    R = copy.deepcopy(R)
    def mv(x):
        strip(R, x)
        for r in R[2:3]:
            for b, es in r['g'].items(): r['g'][b] = [e for e in es if not (e[0] in ('push', 'chg') and e[1] == x)]
        R[3]['g'][POP[x]] = R[3]['g'].get(POP[x], []) + [('ins', 'this', x, -1)]
    for ft in feats:
        if ft == 'A': mv(112)
        if ft == 'B': mv(115)
        if ft == 'D': mv(117)
        if ft == 'E': mv(130)
        if ft == 'C':
            for b, es in R[2]['g'].items(): R[2]['g'][b] = [e for e in es if not (e[0] == 'chg' and e[1] == 103)] if b != 103 else [('push', 103, -1)]
        if ft == 'H':
            g = R[2]['g'][1048]; R[2]['g'][1048] = [e for e in g if not (e[0] == 'chg' and e[1] == 49)]
        if ft == 'F':
            R[3]['g'][126] = [e for e in R[3]['g'][126] if e[0] != 'chg']
        if ft == 'G':
            R[3]['g'][117] = [e for e in R[3]['g'][117] if e[0] != 'chg']
    return R
def fany(Rx, P, restarts=3):
    random.seed(1); best = (999, None)
    for rs in range(restarts):
        f = dict(f0)
        if rs:
            for b in random.sample(BL, 4): f[b] = random.randint(0, 8)
        cur = pot.tinv(hsim.sim(Rx, f, P))
        for _ in range(4):
            ch = False
            for b in BL:
                for v in range(9):
                    g = dict(f); g[b] = v; x = pot.tinv(hsim.sim(Rx, g, P))
                    if x < cur: cur, f, ch = x, g, True
            if not ch: break
        if cur < best[0]: best = (cur, {b: f[b] for b in BL if f[b] != f0[b]})
        if cur == 0: break
    return best
if __name__ == '__main__':
    FE = 'ABCDEFGH'
    print('base', pot.tinv(hsim.sim(Rm, f0, P0)), flush=True)
    for n in range(1, 9):
        for S in itertools.combinations(FE, n):
            r = fany(revert(Rm, S), P0, 2)
            print((r[0], ''.join(S), r[1]), flush=True)
