import sys,r4sim,itertools
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
mv=[int(x) for x in sys.argv[2].split(',')]
keys={}
for v in g.values():
  for e in v:
    if e[0]=='ins' and e[2] in mv: keys[e[2]]=e[3]
base={k:[e for e in v if not(e[0]=='ins' and e[2] in mv)] for k,v in g.items()}
res=[]
Gs=first[:int(sys.argv[3])]
for Gc in itertools.product(Gs,repeat=len(mv)):
  for perm in itertools.permutations(mv):
    gg={x:list(v) for x,v in base.items()}
    for b,G in zip(perm,Gc): gg[G].insert(1,('ins','this',b,keys[b]))
    try:o=r4sim.sim(pre,gg,{})
    except Exception: continue
    res.append((inv(o),list(zip(perm,Gc)),[x for x in o if x in pos][4:]))
res.sort(key=lambda r:r[0])
for r in res[:10]: print(r)
