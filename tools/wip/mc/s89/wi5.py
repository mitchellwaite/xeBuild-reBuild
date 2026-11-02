import sys,r4sim
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
grps=first[:25]; res=[]
for b in T[4:]:
  for G in grps:
    for k in (-1,-2,-3):
      for at in (0,99):
        gg={x:list(v) for x,v in g.items()}; l=gg[G]; l.insert(at if at==0 else len(l),('chg',b,k))
        try:o=r4sim.sim(pre,gg,{})
        except Exception: continue
        res.append((inv(o),b,G,k,at,[x for x in o if x in pos]))
res.sort(key=lambda r:r[0])
for r in res[:12]: print(r)
