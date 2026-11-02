"""wi3.py: insert 77/79 ins events at every position pair within groups GA (and GB) of round 4. python wi3.py SLOT GA GB"""
import sys, copy
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import hsim
R, keys = hsim.load(sys.argv[1]); GA, GB = int(sys.argv[2]), int(sys.argv[3])
T = [35, 42, 53, 77, 79]
g0 = R[3]['g']; ev = {}
for b in g0:
    for e in g0[b]:
        if e[0] == 'ins' and e[2] in (77, 79): ev[e[2]] = e
    g0[b] = [e for e in g0[b] if not (e[0] == 'ins' and e[2] in (77, 79))]
print(GA, g0[GA]); print(GB, g0[GB])
for i in range(len(g0[GA]) + 1):
    for j in range(len(g0[GB]) + 1):
        for a, b in ((77, 79), (79, 77)):
            R2 = copy.deepcopy(R); g = R2[3]['g']
            if GA == GB:
                if j < i: continue
                l = g[GA]; g[GA] = l[:i] + [ev[a]] + l[i:j] + [ev[b]] + l[j:]
            else:
                g[GA] = g[GA][:i] + [ev[a]] + g[GA][i:]; g[GB] = g[GB][:j] + [ev[b]] + g[GB][j:]
            o = hsim.sim(R2, {}, {})
            print(i, j, a, b, [x for x in o if x in T], hsim.inv(o))
