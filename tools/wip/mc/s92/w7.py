import sys,r4sim,random
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
B=[int(x) for x in sys.argv[2].split(',')]; random.seed(3); best=99
for it in range(int(sys.argv[3])):
  ov={b:random.choice((-5,-4,-3,-2,-1,0)) for b in B}
  try:o=r4sim.sim(pre,g,ov)
  except Exception: continue
  v=inv(o)
  if v<best or (v==best and random.random()<.1):
    best=v; print(v,ov,[x for x in o if x in pos],flush=True)
