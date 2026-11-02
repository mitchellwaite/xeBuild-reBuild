import sys, itertools
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86')
import r4sim
pre, g, first = r4sim.load(sys.argv[1])
T = list(map(int, "62 33 29 69 146 128 151 35 42 53 79 81".split()))
B = [146,128,151,35,42,53,79,81,75,83,69]
def score(o):
    i = o.index(143); s = o[i+1:i+1+len(T)]
    return sum(a != b for a, b in zip(s, T))
res = []
for k in range(0, 3):
    for bs in itertools.combinations(B, k):
        for vs in itertools.product([0, -1, -2, -3], repeat=k):
            ov = dict(zip(bs, vs)); ov.setdefault(146, -1)
            o = r4sim.sim(pre, g, ov); res.append((score(o), ov, o[o.index(143)+1:][:14]))
res.sort(key=lambda r: r[0])
for r in res[:15]: print(r)
