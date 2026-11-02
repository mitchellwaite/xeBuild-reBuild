import sys, itertools, r4sim
from r4sim import load
from tmap import target
n=sys.argv[1]; pre,g,first=load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
names=sys.argv[2].split(',')
blks=[m[x] for x in names]
rng=range(int(sys.argv[3]),1)
res=[]
for ks in itertools.product(rng,repeat=len(blks)):
    ov=dict(zip(blks,ks)); o=r4sim.sim(pre,g,ov); res.append((inv(o),ks))
res.sort()
base=r4sim.sim(pre,g,{}); print('base',inv(base))
for r in res[:12]: print(r)
