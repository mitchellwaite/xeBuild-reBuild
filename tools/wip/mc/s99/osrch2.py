# search key overrides + round-3 push order + per-group insert order to hit target
import sys, random, copy
from r4sim import load, sim
from tmap import target
N=sys.argv[1]; pre, g, first = load('d/%s/mc.bbro'%N)
T,_m=target(N+'.c','d/%s/order.txt'%N)
pos={b:i for i,b in enumerate(T)}
i3=max(j for j,e in enumerate(pre) if e==('round',3))
# indices of push pairs (get,push) for low blocks after 48
pp=[j for j in range(i3,len(pre)) if pre[j][0]=='push' and pre[j][2]>-1000]
S=[b for b in T if b not in (T[0],T[1])]
vals=[None,0,-1,-2,-3,-4,-5]
def build(st):
    ov,perm,gp=st
    p=list(pre); seg=[pre[j] for j in pp]
    for k,j in enumerate(pp): p[j]=seg[perm[k]]
    gg={b:[x for x in ([e for e in l] ) ] for b,l in g.items()}
    for b,pr in gp.items():
        l=gg[b]; ins=[e for e in l if e[0]=='ins']; oth=[e for e in l if e[0]!='ins']
        gg[b]=oth+[ins[i] for i in pr]
    return p,gg
def cost(st):
    p,gg=build(st)
    o=sim(p,gg,{k:v for k,v in st[0].items() if v is not None})
    q=[pos[b] for b in o if b in pos]
    inv=sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
    return inv*10+sum(1 for v in st[0].values() if v is not None)+sum(1 for i,x in enumerate(st[1]) if i!=x)+sum(1 for pr in st[2].values() for i,x in enumerate(pr) if i!=x), o
mg={b:len([e for e in l if e[0]=='ins']) for b,l in g.items() if len([e for e in l if e[0]=='ins'])>1}
best=None
for rep in range(int(sys.argv[2])):
    random.seed(rep)
    st=({b:None for b in S},list(range(len(pp))),{b:list(range(n)) for b,n in mg.items()})
    c,o=cost(st); t=20.0
    for it in range(int(sys.argv[3]) if len(sys.argv)>3 else 12000):
        n=copy.deepcopy(st); r=random.random()
        if r<0.5: n[0][random.choice(S)]=random.choice(vals)
        elif r<0.8:
            a,b=random.sample(range(len(pp)),2); n[1][a],n[1][b]=n[1][b],n[1][a]
        else:
            k=random.choice(list(mg)); a,b=random.sample(range(mg[k]),2); n[2][k][a],n[2][k][b]=n[2][k][b],n[2][k][a]
        c2,o2=cost(n)
        if c2<=c or random.random()<pow(2.718,(c-c2)/t): st,c,o=n,c2,o2
        t*=0.9993
    if best is None or c<best[0]: best=(c,st,o)
    print(rep,c,flush=True)
c,st,o=best
print('best',c,{k:v for k,v in st[0].items() if v is not None},[pre[pp[i]][1] for i in st[1]],{k:v for k,v in st[2].items() if v!=list(range(len(v)))})
print(' '.join(str(b) for b in o if b in pos))
