import sys,r4sim,random
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
MV=[int(x) for x in sys.argv[2].split(',')]; B=[int(x) for x in sys.argv[3].split(',')]
nm=int(sys.argv[4]); nk=int(sys.argv[5]); random.seed(int(sys.argv[7]) if len(sys.argv)>7 else 1)
best=99
for it in range(int(sys.argv[6])):
  gg={x:list(v) for x,v in g.items()}; desc=[]
  for b in random.sample(MV,nm):
    G=random.choice(first[:33]); at=random.randint(0,len(gg[G])); k=random.choice((0,0,-1,-2))
    gg[G].insert(at,('ins','this',b,k)); desc.append((b,G,at,k))
  ov={b:random.choice((-3,-2,-1,0)) for b in random.sample(B,nk)} if nk else {}
  try:o=r4sim.sim(pre,gg,ov)
  except Exception: continue
  v=inv(o)
  if v<=best:
    best=v; print(v,desc,ov,[x for x in o if x in pos],flush=True)
