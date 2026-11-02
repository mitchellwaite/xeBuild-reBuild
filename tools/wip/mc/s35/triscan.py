"""triscan.py TAG: tinv of all 3-block f deltas in {-1,+1,+2} on TAG history (hsim); prints best 30."""
import sys, os, itertools
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
R, keys = hsim.load(os.path.join(R0, 'build', 'v', 'mc35', 'slot_' + sys.argv[1]))
f0, P0 = hsim.measured(keys)
BL = [b for b in [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79] if b in f0]
res = []
for bs in itertools.combinations(BL, 3):
    for ds in itertools.product((-1, 1, 2), repeat=3):
        f = dict(f0); ok = True
        for b, d in zip(bs, ds):
            f[b] += d; ok &= f[b] >= 0
        if ok: res.append((pot.tinv(hsim.sim(R, f, P0)), tuple(zip(bs, ds))))
res.sort(); print('n', len(res))
for r in res[:30]: print(r)
