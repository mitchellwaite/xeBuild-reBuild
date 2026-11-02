import sys,r4sim,itertools
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
grps=[b for b in first if b in pos or b in g][:25]
res=[]
D=9001
for G in grps:
  for at in (0,99):
    for k in (-5,-4,-3,-2,-1,0):
      for H in [None]+grps:
        gg={x:list(v) for x,v in g.items()}
        l=gg[G]; l.insert(at if at==0 else len(l),('ins','this',D,k))
        if H is not None:
            if H==G: continue
            gg[H]=gg[H]+[('visit',D)]
        try: o=r4sim.sim(pre,gg,{})
        except Exception as e: continue
        res.append((inv(o),G,at,k,H,[b for b in o if b in pos or b==D]))
res.sort(key=lambda r:r[0])
for r in res[:20]: print(r)
