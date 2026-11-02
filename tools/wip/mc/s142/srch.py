# r4sim targeted search on best16: place 126 after 49, 144 between 55 and 143, 145 after 69
import sys,itertools
sys.path.insert(0,'../s86'); import r4sim
pre,g,first=r4sim.load(sys.argv[1] if len(sys.argv)>1 else 'dd/best16/mc.bbro')
base=r4sim.sim(pre,g); assert base==first
def tgt(o):
    o=list(o)
    for b,after in ((126,49),(144,55),(145,69)):
        o.remove(b); o.insert(o.index(after)+1,b)
    # 108 before 55 retained; 144 after 55 trace
    return o
T=tgt(r4sim.sim(*r4sim.load("dd/best16/mc.bbro")[:2])); print('base',base); print('T',T)
def dist(o):
    n=len(o);m=len(T);d=[[0]*(m+1) for _ in range(n+1)]
    for i in range(n):
        for j in range(m): d[i+1][j+1]=d[i][j]+1 if o[i]==T[j] else max(d[i][j+1],d[i+1][j])
    return m-d[n][m]
keys={}
for e in pre:
    if e[0]=='push': keys[e[1]]=e[2]
    if e[0]=='ins' and e[1]!='this': keys[e[2]]=e[3]
    if e[0]=='chg': keys[e[1]]=e[2]
for v in g.values():
    for e in v:
        if e[0]=='ins': keys.setdefault(e[2],e[3])
        if e[0]=='chg': keys[e[1]]=e[2]
print('d0',dist(base))
for b in (126,121,144,108,55,143,145,128,150,69,49,105,35,42,53,62,33,29):
    print(b,keys.get(b))
cand=[126,121,144,108,55,143,145,128,150,69,49,105,106,35,42,53,62,33,29,152]
ks=[-1000104,-1000304,-1000204,-8,-7,-6,-5,-4,-3,-2,-1,0]
res=[]
for b in cand:
    for k in ks:
        if k==keys.get(b): continue
        try: d=dist(r4sim.sim(pre,g,{b:k}))
        except Exception as ex: continue
        res.append((d,b,k))
res.sort(); print('singles',res[:20])
pr=[]
for (b1,b2) in itertools.combinations(cand,2):
    for k1 in ks:
        for k2 in ks:
            try: d=dist(r4sim.sim(pre,g,{b1:k1,b2:k2}))
            except Exception: continue
            if d<=2: pr.append((d,b1,k1,b2,k2))
pr.sort(); print('pairs',pr[:40])
