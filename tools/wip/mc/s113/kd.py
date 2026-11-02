# kd.py dmp seed push : 141 pushed with key, then single/double edits (tail key ov, dummy nodes)
import sys, itertools
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s111')
from wi import *
pre, g, first = r4sim.load(sys.argv[1])
pk = int(sys.argv[2]); P = push141(pre, pk) if pk else pre
base = srch.sim(P,g); print('base', srch.dist(base))
blocks = sorted(set(base))
keys = list(range(-12, 2)) + [-1000000, -1000100, -1000200]
pts = [('p', i) for i in range(len(P)-60, len(P)+1)] + [(b, j) for b in g for j in range(len(g[b])+1)]
ed = [('ov',b,k) for b in blocks for k in keys] + [('dum',p,k) for p in pts for k in (-12,-8,-5,-4,-3,-2,-1,0,1)]
def ev(es):
    ov={};du={}
    for e in es: (ov if e[0]=='ov' else du)[e[1]]=e[2]
    return srch.dist(srch.sim(P,g,ov,du))
res = sorted(((ev([e]), e) for e in ed), key=lambda r: r[0])
print(res[:15])
s = [e for d,e in res if d < srch.dist(base)][:150]
r2 = sorted(((ev([a,b]),a,b) for a,b in itertools.combinations(s,2)), key=lambda r: r[0])
print(r2[:15])
