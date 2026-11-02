import sys,itertools,nm,sim3
TAG=sys.argv[1]; OV0=eval(sys.argv[2]); ds=eval(sys.argv[3])
pre,g3,f3,g4,f4=sim3.load('../../../../build/v/aio_p1/%s/aio.bbro'%TAG)
k=f4.index(74); TARGET=f4[:k]+nm.REF4; idx={h:i for i,h in enumerate(TARGET)}
def score(ov):
    G4={b:list(v) for b,v in g4.items()}
    n=0
    for d in ds:
        n+=1; G4.setdefault(d[1],[]).insert(min(d[2],len(G4[d[1]])),('ins','this',9000+n,d[3]))
    o3,o4=sim3.sim(pre,g3,G4,ov)
    v=[idx[h] for h in o4 if h in idx]
    return sum(1 for i in range(len(v)) for j in range(i+1,len(v)) if v[i]>v[j])
print('base',score(OV0))
cand=[(b,-3) for b in (167,177,218,208,157)]+[(b,-5) for b in (167,177,218,208,157)]+[(230,-1),(230,-3)]
R=[]
for n in (1,2,3):
    for c in itertools.combinations(cand,n):
        o=dict(OV0); o.update(dict(c)); R.append((score(o),n,c))
R.sort(key=lambda x:x[:2]); print(R[:10])
