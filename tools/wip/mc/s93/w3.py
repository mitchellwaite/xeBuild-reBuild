import sys,r4sim,random
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
mv=[78,80]
base={k:[e for e in v if not(e[0]=='ins' and e[2] in mv)] for k,v in g.items()}
B=[int(x) for x in sys.argv[2].split(',')]; nk=int(sys.argv[3]); random.seed(1)
best=99;seen=set()
for it in range(int(sys.argv[4])):
  G=random.choice(first[:int(sys.argv[5])]); at=random.randint(0,len(base[G])); od=random.choice(((78,80),(80,78)))
  ov={b:random.choice((-3,-2,-1,0)) for b in random.sample(B,nk)}
  gg={x:list(v) for x,v in base.items()}
  for b in reversed(od): gg[G].insert(at,('ins','this',b,0))
  try:o=r4sim.sim(pre,gg,ov)
  except Exception: continue
  v=inv(o)
  if v<=best:
    best=v; print(v,G,at,od,ov,[x for x in o if x in pos],flush=True)
