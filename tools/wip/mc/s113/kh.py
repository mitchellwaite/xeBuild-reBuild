# kh.py dmp seed : SA over {extra round-3 push of an r4-visited block, key override of r4 nodes}, min dist
import sys, random
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s111')
from wi import *
pre, g, first = r4sim.load(sys.argv[1]); random.seed(int(sys.argv[2]))
vs = sorted({e[1] for b in g for e in g[b] if e[0]=='visit'} - set(first) - {e[1] for e in pre if e[0] in ('push','get')} - {e[2] for e in pre if e[0]=='ins'})
i3 = max(i for i,e in enumerate(pre) if e==('round',3))
r4 = sorted(set(first))
def K(p,f): return -(1000000+100*p+f) if p else -f
KS=[K(p,f) for p in range(0,6) for f in range(0,13)]
def ev(E):
    Q=list(pre); ov={}
    for e in sorted([e for e in E if e[0]=='p'], key=lambda e:-e[1]): Q.insert(e[1], ('push', e[2], e[3]))
    for e in E:
        if e[0]=='o': ov[e[1]]=e[2]
    o=srch.sim(Q,g,ov); return srch.dist(o)+len(set(o)-set(srch.T))+abs(len(o)-len(set(o)))
def rnd():
    if random.random()<0.5: return ('p', random.randint(i3+1,len(pre)), random.choice(vs), random.choice(KS))
    return ('o', random.choice(r4), random.choice(KS))
best=(99,); cur=[]; dc=ev(cur)
for it in range(20000):
    E=list(cur); r=random.random()
    if r<0.3 and E: E.pop(random.randrange(len(E)))
    elif r<0.6 and E: E[random.randrange(len(E))]=rnd()
    elif len(E)<4: E.append(rnd())
    d=ev(E)
    if d<dc or (d==dc and len(E)<=len(cur)) or random.random()<0.02: cur,dc=E,d
    if (d,len(E))<best[:2]: best=(d,len(E),E); print(best,flush=True)
