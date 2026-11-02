"""wi9.py SLOT: dummy node D (key k) inserted in a round-4 group at pos i, deleted (visited) later at (G2,j). keeps -r pushes."""
import sys, copy
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import hsim
R, keys = hsim.load(sys.argv[1])
T = [35, 42, 53, 77, 79]
g0 = R[3]['g']; G = list(g0)
GA = [x for x in G[G.index(49):G.index(67) + 1]]
res = []
for ga in GA:
    for i in range(len(g0[ga]) + 1):
        for gb in [None] + GA[GA.index(ga):]:
            for j in (range(len(g0[gb]) + 1) if gb else [None]):
                if gb == ga and j <= i: continue
                for k in (0, -1, -2, -3):
                    R2 = copy.deepcopy(R); g = R2[3]['g']
                    if gb is not None: g[gb] = g[gb][:j] + [('visit', 9999)] + g[gb][j:]
                    g[ga] = g[ga][:i] + [('ins', 'this', 9999, k)] + g[ga][i:]
                    o = hsim.sim(R2, {}, {})
                    t = [x for x in o if x in T]
                    res.append((t != T, hsim.inv(o), ga, i, gb, j, k, t))
res.sort(key=lambda r: (r[0], r[1]))
for r in res[:20]: print(r)
