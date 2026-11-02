import sys,r4sim,itertools
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
B=[int(x) for x in sys.argv[2].split(',')]
res=[]
for ks in itertools.product((-4,-3,-2,-1,0),repeat=len(B)):
  ov=dict(zip(B,ks))
  try:o=r4sim.sim(pre,g,ov)
  except Exception: continue
  res.append((inv(o),ks,[x for x in o if x in pos]))
res.sort(key=lambda r:r[0])
for r in res[:10]: print(r)
