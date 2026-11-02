# kv.py dmp push141key : extra round-3 push of a block later visited in round 4 (deleted from heap), single and pairs
import sys, itertools
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s111')
from wi import *
pre, g, first = r4sim.load(sys.argv[1])
pk = int(sys.argv[2]); P = push141(pre, pk) if pk else pre
vs = sorted({e[1] for b in g for e in g[b] if e[0]=='visit'})
print('visited-in-r4', vs)
i3 = max(i for i,e in enumerate(P) if e==('round',3))
def mk(edits):
    Q = list(P)
    for (i,v,k) in sorted(edits, reverse=True): Q.insert(i, ('push', v, k))
    return Q
ks = [-12,-9,-7,-5,-4,-3,-2,-1,0,-1000100,-1000105,-1000200,-1000205,-1000300]
res=[]
for i in range(i3+1, len(P)+1):
    for v in vs:
        for k in ks:
            o = srch.sim(mk([(i,v,k)]), g); res.append((srch.dist(o), i, v, k))
res.sort(); print(res[:20])
