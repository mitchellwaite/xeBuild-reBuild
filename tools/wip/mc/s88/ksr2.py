import sys, itertools, r4sim
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}; iv={v:k for k,v in m.items()}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
D={}
for a in sys.argv[2:]:
    k,v=a.split('='); D[m[k]]=[int(x) for x in v.split(',')]
res=[]
for ks in itertools.product(*D.values()):
    ov=dict(zip(D,ks)); o=r4sim.sim(pre,g,ov); res.append((inv(o),ks,' '.join(iv.get(b,'?') for b in o if b in pos)))
res.sort()
print([iv[b] for b in D])
for r in res[:10]: print(r)
