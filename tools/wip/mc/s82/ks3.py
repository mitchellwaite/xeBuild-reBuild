import sys, random
from r4sim import load, sim
pre, g, first = load('d/%s/mc.bbro'%sys.argv[1])
from tmap import target
T,_=target(sys.argv[1]+'.c','d/%s/order.txt'%sys.argv[1])
pos={b:i for i,b in enumerate(T)}
S=T[1:]
vals=[None,0,-1000000]
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
def cost(ov):
    return inv(sim(pre,g,{k:v for k,v in ov.items() if v is not None}))*100+sum(v is not None for v in ov.values())
print('base inv',inv(first))
best=None
for rep in range(int(sys.argv[2]) if len(sys.argv)>2 else 6):
    random.seed(rep); ov={b:None for b in S}; c=cost(ov); t=20.0
    for it in range(int(sys.argv[4]) if len(sys.argv)>4 else 6000):
        b=random.choice(S); old=ov[b]; ov[b]=random.choice(vals); c2=cost(ov)
        if c2<=c or random.random()<pow(2.718,(c-c2)/t): c=c2
        else: ov[b]=old
        t*=0.999
    if best is None or c<best[0]: best=(c,dict(ov))
print('best',best[0],{k:v for k,v in best[1].items() if v is not None})
o=sim(pre,g,{k:v for k,v in best[1].items() if v is not None}); print(' '.join(str(b) for b in o if b in pos))
