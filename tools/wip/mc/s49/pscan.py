"""pscan.py A: on A's history, scan trace-end priority P (0..3) and f (0..4) for 55,126,125,61; best inv."""
import sys, os, itertools
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R0, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.join(R0, r'tools\wip'))
import hsim
Ra, ka = hsim.load(sys.argv[1]); fa, Pa = hsim.measured(ka)
B = [55, 126, 125, 61]; res = []
for Ps in itertools.product(range(3), repeat=4):
    for fs in itertools.product(range(1, 5), repeat=4):
        f, P = dict(fa), dict(Pa)
        for b, p, v in zip(B, Ps, fs): P[b] = p; f[b] = v
        o = hsim.sim(Ra, f, P); res.append((hsim.inv(o), Ps, fs, o))
res.sort(key=lambda x: x[0])
for r in res[:5]: print(r[0], r[1], r[2], ' '.join(map(str, r[3])))
