import sys,itertools,nm,sim3
TAG=sys.argv[1]; OV0=eval(sys.argv[2])
pre,g3,f3,g4,f4=sim3.load('../../../../build/v/aio_p1/%s/aio.bbro'%TAG)
k=f4.index(74); TARGET=f4[:k]+nm.REF4; idx={h:i for i,h in enumerate(TARGET)}
def score(ds,ov=OV0):
    G4={b:list(v) for b,v in g4.items()}
    n=0
    for d in ds:
        n+=1; l=G4.setdefault(d[1],[]); l.insert(min(d[2],len(l)),('ins','this',9000+n,d[3]))
    o3,o4=sim3.sim(pre,g3,G4,ov)
    v=[idx[h] for h in o4 if h in idx]
    return sum(1 for i in range(len(v)) for j in range(i+1,len(v)) if v[i]>v[j])
# single/pair dummies only at the given sites
SITES=eval(sys.argv[3])
KS=[0,-1,-2,-4,-8,-12,-17,-18,-19,-20,-25,-30,-37,-38,-40,-50,-60,-80]
ms=[('r4',b,p,k_) for b,p in SITES for k_ in KS]
R=[]
for a,b in itertools.combinations(ms,2):
    R.append((score([a,b]),a,b))
R.sort(key=lambda x:x[0])
print(R[:14])
