"""wi8.py SLOT: place ins of 77 and 79 independently at any (group,pos) in round 4 (groups 55.. up to 73)."""
import sys, copy, itertools
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import hsim
R, keys = hsim.load(sys.argv[1])
T = [35, 42, 53, 77, 79]
g0 = R[3]['g']; ev = {}
for b in g0:
    for e in g0[b]:
        if e[0] == 'ins' and e[2] in (77, 79): ev[e[2]] = e
    g0[b] = [e for e in g0[b] if not (e[0] == 'ins' and e[2] in (77, 79))]
GS = [G for G in g0 if G in (55, 61, 33, 29, 67, 127, 117, 130, 49, 115, 112, 103, 126, 125, 121, 116)]
P = [(G, i) for G in GS for i in range(len(g0[G]) + 1)]
res = []
for p7 in P:
    for p9 in P:
        for first in (77, 79):
            R2 = copy.deepcopy(R); g = R2[3]['g']
            ins = {}
            for b, (G, i) in ((77, p7), (79, p9)): ins.setdefault(G, []).append((i, b))
            for G, l in ins.items():
                l.sort(key=lambda x: (x[0], x[1] != first))
                L = g[G]; out = []
                for k in range(len(L) + 1):
                    for (i, b) in l:
                        if i == k: out.append(ev[b])
                    if k < len(L): out.append(L[k])
                g[G] = out
            o = hsim.sim(R2, {}, {})
            res.append((hsim.inv(o), p7, p9, first, [x for x in o if x in T]))
res.sort()
for r in res[:25]: print(r)
