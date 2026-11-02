import sys, itertools, r4sim
from r4sim import load
pre,g,first=load("d/%s/mc.bbro"%sys.argv[2])
from tmap import target; T,_=target(sys.argv[2]+".c","d/%s/order.txt"%sys.argv[2])
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
# slots: all ins events in groups before 145 get
order=first[:first.index(T[0])]
slots=[(b,k) for b in order for k,e in enumerate(g.get(b,[])) if e[0]=='ins' and e[2] in pos]
evs=[g[b][k] for b,k in slots]
print(len(slots),[e[2] for e in evs])
res=[]
for p in itertools.permutations(range(len(evs))):
    gg={k:list(v) for k,v in g.items()}
    for (b,k),j in zip(slots,p): gg[b][k]=evs[j]
    o=r4sim.sim(pre,gg,{}); res.append((inv(o),[evs[j][2] for j in p],[b for b in o if b in pos]))
res.sort(key=lambda x:x[0])
for r in res[:10]: print(r)
print('--- with 78/80 swapped in their group')
for b,l in g.items():
    i=[k for k,e in enumerate(l) if e[0]=='ins' and e[2] in(78,80)]
    if len(i)==2: l[i[0]],l[i[1]]=l[i[1]],l[i[0]]; print('grp',b)
res=[]
for p in itertools.permutations(range(len(evs))):
    gg={k:list(v) for k,v in g.items()}
    for (b,k),j in zip(slots,p): gg[b][k]=evs[j]
    o=r4sim.sim(pre,gg,{}); res.append((inv(o),[evs[j][2] for j in p],[b for b in o if b in pos]))
res.sort(key=lambda x:x[0])
for r in res[:5]: print(r)
