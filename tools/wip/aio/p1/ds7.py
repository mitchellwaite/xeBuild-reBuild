"""ds7.py TAG 'ov' TL WIDTH SEED: beam over dummies in r3/r4 groups with sim3 (dynamic r3)."""
import sys,os,time,random
import nm,sim3
TAG=sys.argv[1]; OV=eval(sys.argv[2]); TL=float(sys.argv[3]); W=int(sys.argv[4]); random.seed(int(sys.argv[5]))
pre,g3,f3,g4,f4=sim3.load('../../../../build/v/aio_p1/%s/aio.bbro'%TAG)
k=f4.index(74)
TARGET=f4[:k]+nm.REF4
idx={h:i for i,h in enumerate(TARGET)}
U=set(77+5*i for i in range(11))
F3=[b for b in f3 if b not in U]
def score(ds,ov=OV):
    a=[dict() ,dict()]
    G3=g3;G4=g4
    if ds:
        G3={b:list(v) for b,v in g3.items()}; G4={b:list(v) for b,v in g4.items()}
    n=0
    for d in ds:
        n+=1; id_=9000+n
        if d[0]=='r3':
            G3.setdefault(d[1],[])
            l=G3[d[1]]
            if d[3]>=-89:  # too cold for round 3: pushed to round 4 at once
                l.insert(min(d[2],len(l)),('push',id_,d[3]))
            else:
                l.insert(min(d[2],len(l)),('ins','this',id_,d[3]))
        else:
            l=G4.setdefault(d[1],[]); l.insert(min(d[2],len(l)),('ins','this',id_,d[3]))
    o3,o4=sim3.sim(pre,G3,G4,ov)
    p=0
    if [b for b in o3 if b not in U and b<9000]!=F3: p=100
    s=[h for h in o4 if h in idx]
    v=[idx[h] for h in s]
    return p+sum(1 for i in range(len(v)) for j in range(i+1,len(v)) if v[i]>v[j])
K3=[0,-4,-19,-37,-60,-95,-132,-249,-300]
K4=[0,-4,-8,-19,-37,-38,-200]
moves=[('r3',b,p,key) for b in f3 for p in (0,99) for key in K3]+[('r4',b,p,key) for b in f4 for p in (0,99) for key in K4]
print(len(moves),'base',score([]),flush=True)
t=time.time(); beam=[[]]; seen=set(); best=(999,None); depth=0
while time.time()-t<TL and depth<7:
    cand=[]
    for ds in beam:
        ms=list(moves); random.shuffle(ms)
        for m in ms[:int(os.environ.get('MM','1100'))]:
            d=ds+[m]; f=frozenset(d)
            if f in seen: continue
            seen.add(f); cand.append((score(d),d))
            if time.time()-t>TL: break
    if not cand: break
    cand.sort(key=lambda x:(x[0],len(x[1])))
    beam=[d for s,d in cand[:W]]
    if cand[0][0]<best[0]: best=cand[0]
    print(depth,len(cand),cand[0],'%.0fs'%(time.time()-t),flush=True)
    depth+=1
    if best[0]==0: break
print('BEST',best)
