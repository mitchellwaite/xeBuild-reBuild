import sys, itertools, r4sim, random
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
R=dict(x.split('=') for x in sys.argv[3:]) 
keys={int(k):[int(a) for a in v.split(',')] for k,v in R.items()}
res=[]
for ks in itertools.product(*keys.values()):
    ov=dict(zip(keys,ks)); o=r4sim.sim(pre,g,ov); res.append((inv(o),ks,[b for b in o if b in pos]))
res.sort(key=lambda x:x[0])
print(list(keys))
for r in res[:int(sys.argv[2])]: print(r)
