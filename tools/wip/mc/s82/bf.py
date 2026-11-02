import sys, itertools
from r4sim import load, sim
pre,g,first=load('d/b0/mc.bbro')
T=[145,49,125,121,107,55,139,138,61,33,29,68,140,127,143,35,42,53,78,80,74]
pos={b:i for i,b in enumerate(T)}
F={49:-14,125:-13,121:-11,107:-10,55:-9,139:-8,138:-7,61:-5,33:-4,29:-3,68:-2}
B=[140,127,143,35,42,53,78,80,74]
res=[]
for vs in itertools.product([0,-1],repeat=len(B)):
    ov=dict(F); ov.update(zip(B,vs))
    o=[b for b in sim(pre,g,ov) if b in pos]; q=[pos[b] for b in o]
    inv=sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
    res.append((inv,vs,o))
res.sort(key=lambda r:r[0])
for r in res[:8]: print(r[0],dict(zip(B,r[1])),' '.join(map(str,r[2][11:])))
