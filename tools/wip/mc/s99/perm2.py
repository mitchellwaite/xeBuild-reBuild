import sys, itertools, r4sim
from r4sim import load
pre,g0,first=load(sys.argv[1])
T=[145,49,125,121,107,55,139,138,61,33,29,68,140,127,143,35,42,53,78,80,74]
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
P=[int(x) for x in sys.argv[2].split(',')]  # desired init-insert order
for mvgrp in [None]+first[:30]:
  for blk in (78,80):
    g={k:list(v) for k,v in g0.items()}
    if mvgrp is not None:
        for k in g: g[k]=[e for e in g[k] if not(e[0]=='ins' and e[2]==blk)]
        g.setdefault(mvgrp,[]).insert(0,('ins','this',blk,0))
    order=first[:first.index(145)]
    slots=[(b,k) for b in order for k,e in enumerate(g.get(b,[])) if e[0]=='ins' and e[2] in pos and e[2] in P]
    byb={g[b][k][2]:g[b][k] for b,k in slots}
    for (b,k),x in zip(slots,P): g[b][k]=byb[x]
    o=r4sim.sim(pre,g,{}); i=inv(o)
    if i<=8: print(i,mvgrp,blk,[b for b in o if b in pos])
