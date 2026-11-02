import sys, r4sim, random
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
B=[int(x) for x in sys.argv[3].split(',')]
grps=first[:30]
def run(moves):
    p=list(pre); gg={k:list(v) for k,v in g.items()}
    for b,dst,k,at in moves:
        for kk in gg: gg[kk]=[e for e in gg[kk] if not(e[0]=='ins' and e[2]==b)]
        p=[e for e in p if not(e[0]=='push' and e[1]==b)]
        l=gg.setdefault(dst,[]); l.insert(0 if at==0 else len(l),('ins','this',b,k))
    return r4sim.sim(p,gg,{})
random.seed(int(sys.argv[4]) if len(sys.argv)>4 else 1)
res={}
for it in range(int(sys.argv[2])):
    mv=[]
    for b in random.sample(B,random.randint(1,min(int(sys.argv[5]) if len(sys.argv)>5 else 3,len(B)))):
        mv.append((b,random.choice([x for x in grps if x!=b]),random.randint(-4,0),random.randint(0,1)))
    try: o=run(mv)
    except Exception: continue
    if len([b for b in o if b in pos])<len(T): continue
    v=inv(o); key=tuple(sorted(mv))
    res[key]=(v,len(mv),[b for b in o if b in pos])
for k,v in sorted(res.items(),key=lambda x:(x[1][0],x[1][1]))[:15]: print(v[0],k,v[2])
