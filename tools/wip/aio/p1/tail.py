import sys,itertools,nm,sim3
TAG=sys.argv[1]
pre,g3,f3,g4,f4=sim3.load('../../../../build/v/aio_p1/%s/aio.bbro'%TAG)
print(f4==sim3.sim(pre,g3,g4)[1])
tg=eval(sys.argv[2])
def sc(ov,ds=()):
    G4={b:list(v) for b,v in g4.items()}
    n=0
    for d in ds:
        n+=1; l=G4.setdefault(d[1],[]); l.insert(min(d[2],len(l)),('ins','this',9000+n,d[3]))
    o=sim3.sim(pre,g3,G4,ov)[1]
    s=[h for h in o if h in tg]
    return sum(1 for i in range(len(s)) for j in range(i+1,len(s)) if tg.index(s[i])>tg.index(s[j])),[h for h in o if h<9000]==[h for h in o if h<9000 and h not in tg][:0]
print(sc({}))
R=[]
for a in (47,37,17,57,7,67,241):
    for k in (-9,-7,-6,-5):
        R.append((sc({a:k})[0],a,k))
R.sort();print(R[:6])
heads=[h for h in f4]
R=[]
for b in heads:
  for p in (0,99):
    for k in (0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11):
        R.append((sc({},[('r4',b,p,k)])[0],b,p,k))
R.sort();print(R[:12])
