"""wi7.py SLOT: move 77/79 ins events into each round-4 group before 55 (79 first), all positions."""
import sys, copy
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import hsim
R, keys = hsim.load(sys.argv[1])
T = [35, 42, 53, 77, 79]
g0 = R[3]['g']; ev = {}
for b in g0:
    for e in g0[b]:
        if e[0] == 'ins' and e[2] in (77, 79): ev[e[2]] = e
    g0[b] = [e for e in g0[b] if not (e[0] == 'ins' and e[2] in (77, 79))]
for G in list(g0):
    if G == 55: break
    n = len(g0[G])
    for i in range(n + 1):
        for j in range(i, n + 1):
            for a, b in ((79, 77), (77, 79)):
                R2 = copy.deepcopy(R); l = R2[3]['g'][G]
                R2[3]['g'][G] = l[:i] + [ev[a]] + l[i:j] + [ev[b]] + l[j:]
                o = hsim.sim(R2, {}, {})
                print(G, i, j, a, b, [x for x in o if x in T], hsim.inv(o))
