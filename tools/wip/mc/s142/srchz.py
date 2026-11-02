import sys
sys.path.insert(0,'../s86'); import r4sim
pre,g,first=r4sim.load(sys.argv[1])
base=r4sim.sim(pre,g); assert base==first
tail=[int(x) for x in sys.argv[2].split()]
i=base.index(69)+1; rest=[b for b in base[i:] if b not in tail]
T=base[:i]+tail+rest
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
