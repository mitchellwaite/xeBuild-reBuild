import sys
sys.path.insert(0,'../s104'); sys.path.insert(0,'../s86')
import srch, r4sim, m, itertools
pre,g,first=r4sim.load(sys.argv[1])
blks=set(map(int,sys.argv[2].split(',')))
res=[]
for e,p2,g2 in m.edits(pre,g):
    if e[0]=='mvi' and e[1] in blks and e[2] in (134,) or e[0]=='dum':
        res.append((srch.dist(srch.sim(p2,g2)),e))
# also all key combos for blks inside 134 group
ev=g[134]
res.sort(key=lambda r:r[0]); print(res[:15])
idx={e[2]:j for j,e in enumerate(ev) if e[0]=='ins'}
for ks in itertools.product(range(-4,1),repeat=len(idx)):
    l=list(ev)
    for (b,j),k in zip(idx.items(),ks): l[j]=('ins','this',b,k)
    g2=dict(g); g2[134]=l; d=srch.dist(srch.sim(pre,g2))
    if d<=2: print(dict(zip(idx,ks)),d)
