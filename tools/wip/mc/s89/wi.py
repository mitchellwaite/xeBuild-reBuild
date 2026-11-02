import sys,r4sim,itertools
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
bs=[int(x) for x in sys.argv[2].split(',')]
res=[]
for ks in itertools.product(range(-5,1),repeat=len(bs)):
    ov=dict(zip(bs,ks))
    # also override 'this' inserts via ov in sim
    o=r4sim.sim(pre,g,ov); res.append((inv(o),ks,[b for b in o if b in pos]))
res.sort()
for r in res[:12]: print(r)
print('T',T)
