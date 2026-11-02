"""fany.py TAG : can ANY f assignment (blocks of the tail, 0..8) give 0 inversions on TAG's history?
random-restart coordinate descent in hsim."""
import sys, os, random
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
Rr, keys = hsim.load(os.path.join(R, 'build', 'v', 'mc27', 'slot_' + sys.argv[1]))
f0, P0 = hsim.measured(keys)
BL = [b for b in [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79] if b in f0]
random.seed(1); best = (999,)
for rs in range(int(sys.argv[2]) if len(sys.argv) > 2 else 30):
    f = dict(f0)
    if rs: 
        for b in random.sample(BL, 4): f[b] = random.randint(0, 8)
    cur = pot.tinv(hsim.sim(Rr, f, P0))
    for _ in range(4):
        for b in BL:
            for v in range(0, 9):
                g = dict(f); g[b] = v; x = pot.tinv(hsim.sim(Rr, g, P0))
                if x < cur: cur, f = x, g
    if cur < best[0]:
        best = (cur, {b: f[b] for b in BL if f[b] != f0[b]}, ' '.join(map(str, hsim.sim(Rr, f, P0)[12:])))
        print(best, flush=True)
