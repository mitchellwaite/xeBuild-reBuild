import sys, itertools
sys.path.insert(0,'../s104'); sys.path.insert(0,'../s86')
import srch, r4sim
pre,g,first=r4sim.load(sys.argv[1]); B=list(map(int,sys.argv[2].split(',')))
base={}
for e in pre:
    if e[0] in('push',) and e[1] in B: base[e[1]]=e[2]
for b in g:
    for e in g[b]:
        if e[0]=='ins' and e[2] in B: base[e[2]]=e[3]
res=[]
for ks in itertools.product(range(-4,1),repeat=len(B)):
    ov=dict(zip(B,ks)); o=srch.sim(pre,g,ov); d=srch.dist(o)
    nch=sum(1 for b in B if ov[b]!=base.get(b))
    res.append((d,nch,ov))
res.sort(key=lambda r:(r[0],r[1]))
print('base',base)
for r in res[:15]: print(r)
