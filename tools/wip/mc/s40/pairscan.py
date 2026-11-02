"""pairscan.py TAG: tinv of all 1-,2-,3-block f deltas (-2..+3) on TAG history (hsim)."""
import sys, os, itertools
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
R, keys = hsim.load(os.path.join(R0, 'build', 'v', 'mc40', 'slot_' + sys.argv[1]))
f0, P0 = hsim.measured(keys)
BL = [b for b in [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79] if b in f0]
D = [d for d in range(-2, 4) if d]
res = []
def ev(ch):
    f = dict(f0)
    for b, d in ch:
        f[b] = f0[b] + d
        if f[b] < 0: return
    res.append((pot.tinv(hsim.sim(R, f, P0)), ch))
for k in (1, 2):
    for bs in itertools.combinations(BL, k):
        for ds in itertools.product(D, repeat=k): ev(tuple(zip(bs, ds)))
res.sort(); print('base', pot.tinv(hsim.sim(R, f0, P0)), 'n', len(res))
for r in res[:25]: print(r)
