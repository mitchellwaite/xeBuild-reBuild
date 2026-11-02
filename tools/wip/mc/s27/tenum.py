"""tenum.py TAG : exhaustive hsim over f of non-loop tail blocks (+RX126/RX117 chains via RXEV)."""
import sys, os, itertools
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18'))
import hsim
sd = os.path.join(R, 'build', 'v', 'mc27', 'slot_' + sys.argv[1])
Rr, keys = hsim.load(sd)
f0, P0 = hsim.measured(keys)
BL = [126, 125, 127, 117, 130]
res = []
for rx in [(), ('126:125',), ('117:130',), ('126:125', '117:130')]:
    hsim.RXEV.clear()
    for it in rx:
        s, t = map(int, it.split(':')); hsim.RXEV.setdefault(s, []).append(t)
    for vals in itertools.product(range(3), repeat=len(BL)):
        f = dict(f0); P = dict(P0)
        for b, v in zip(BL, vals): f[b] = v
        if '126:125' in rx: P[125] = 1 if f[126] >= 1 else 0
        if '117:130' in rx: P[130] = 1 if f[117] >= 1 else 0
        o = hsim.sim(Rr, f, P)
        res.append((hsim.inv(o), rx, vals, ' '.join(map(str, o[11:]))))
res.sort()
for r in res[:15]: print(r)
