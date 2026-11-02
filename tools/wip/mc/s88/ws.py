# what-if search on NAME: keys of R4-inserted front blocks + ins-order perms in groups + moving ins events between groups
import sys, itertools, r4sim
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
blocks=[55,140,139,62,69,141]
cur={}
for b,l in g.items():
    for e in l:
        if e[0]=='ins' and e[2] in blocks: cur[e[2]]=(b,e[3])
print(cur)
grps=[b for b in first if b in g]
res=[]
import random
random.seed(1)
for it in range(int(sys.argv[2])):
    gg={k:list(v) for k,v in g.items()}
    desc=[]
    nm=random.randint(0,3)
    for b in random.sample(blocks,nm):
        k=random.randint(-4,0); dst=random.choice(grps[:20]); 
        for kk in gg: gg[kk]=[e for e in gg[kk] if not(e[0]=='ins' and e[2]==b)]
        p=random.randint(0,len(gg[dst])); gg[dst].insert(p,('ins','this',b,k)); desc.append((b,dst,p,k))
    o=r4sim.sim(pre,gg,{}); res.append((inv(o),len(desc),desc))
res.sort(key=lambda x:(x[0],x[1]))
for r in res[:15]: print(r)
