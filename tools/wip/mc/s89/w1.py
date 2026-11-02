import sys,r4sim,itertools
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
mv=[78,80]
base={k:[e for e in v if not(e[0]=='ins' and e[2] in mv)] for k,v in g.items()}
res=[]
o=r4sim.sim(pre,base,{}); print('drop only',inv(o),[b for b in o if b in pos])
for G in first[:33]:
 for k78 in (0,-1,-2,-3):
  for k80 in (0,-1,-2,-3):
   for at in range(len(base[G])+1):
    for order in ((78,80),(80,78)):
     gg={x:list(v) for x,v in base.items()}; l=gg[G]
     for b in reversed(order): l.insert(at,('ins','this',b,{78:k78,80:k80}[b]))
     try:o=r4sim.sim(pre,gg,{})
     except Exception: continue
     res.append((inv(o),G,k78,k80,at,order,[x for x in o if x in pos]))
res.sort(key=lambda r:r[0])
for r in res[:15]: print(r)
