import sys,itertools,random
sys.path.insert(0,'../s86'); import r4sim
pre,g,first=r4sim.load('dd/vEa/mc.bbro')
T=[int(x) for x in "147 96 113 117 120 123 116 131 132 139 146 134 152 49 127 122 108 55 144 143 62 33 29 69 145 129 150 35 42 53 81 79 75 83 88 160 97 161 98 93 95".split()]
def dist(o):
    s=[b for b in o if b in T]; 
    # LCS distance
    n=len(s);m=len(T);d=[[0]*(m+1) for _ in range(n+1)]
    for i in range(n):
        for j in range(m): d[i+1][j+1]=d[i][j]+1 if s[i]==T[j] else max(d[i][j+1],d[i+1][j])
    return len(T)-d[n][m] + (len(T)-n)
keys={}
for e in pre:
    if e[0]=='push': keys[e[1]]=e[2]
    if e[0]=='ins' and e[1]!='this': keys[e[2]]=e[3]
    if e[0]=='chg': keys[e[1]]=e[2]
for v in g.values():
    for e in v:
        if e[0]=='ins': keys.setdefault(e[2],e[3])
print('base',dist(r4sim.sim(pre,g)))
print('keys',sorted(keys.items())[:5], len(keys))
ks=sorted(set(keys.values()))
blocks=list(keys)
res=[]
for b in blocks:
    for k in ks:
        if k==keys[b]: continue
        try: d=dist(r4sim.sim(pre,g,{b:k}))
        except Exception: continue
        res.append((d,b,k))
res.sort(); print('singles',res[:15])
import math
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
ks2=sorted(set(ks+[k+1 for k in ks]+[k-1 for k in ks]))
best=None
for run in range(6):
    ov={};cur=dist(r4sim.sim(pre,g));Tm=3.0
    for it in range(4000):
        o=dict(ov); r=random.random()
        if r<0.6 or not o: o[random.choice(blocks)]=random.choice(ks2)
        elif r<0.85: o.pop(random.choice(list(o)))
        else: b=random.choice(list(o)); o[b]=random.choice(ks2)
        try: d=dist(r4sim.sim(pre,g,o))
        except Exception: continue
        c=d+0.3*len(o); cc=cur+0.3*len(ov)
        if c<=cc or random.random()<math.exp((cc-c)/Tm): ov,cur=o,d
        Tm=max(0.05,Tm*0.999)
        if best is None or (d,len(ov))<best[:2]: best=(d,len(ov),dict(ov))
    print(run,cur,len(ov),best[:2],flush=True)
print('BEST',best)
