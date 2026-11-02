"""ds.py TAG: search dummy heap entries + key options in r4sim model for REF order"""
import sys,random,nm,r4sim,itertools,time
pre,g,first=r4sim.load('../../../../build/v/aio_p1/%s/aio.bbro'%sys.argv[1])
k=first.index(74)
TARGET=first[:k]+nm.REF4
TS=set(TARGET)
def score(ov,dums):
    g2={b:list(v) for b,v in g.items()}
    for i,(b,pos,key) in enumerate(dums):
        l=g2.setdefault(b,[])
        l.insert(min(pos,len(l)),('ins','this',9000+i,key))
    # dummy may also be pushed in pre: skip
    o=r4sim.sim(pre,g2,ov)
    s=[h for h in o if h in TS]
    d=sum(a!=b for a,b in zip(s,TARGET))
    # inversions
    idx={h:i for i,h in enumerate(TARGET)}
    v=[idx[h] for h in s]
    inv=sum(1 for i in range(len(v)) for j in range(i+1,len(v)) if v[i]>v[j])
    return inv,d,s
BASEOV=[{259:-38,229:-15},{259:-37,229:-15},{259:-38,229:-19},{259:-37,229:-19},{259:-38,229:-16},{259:-37,229:-16},{259:-38,27:-11},{259:-37,27:-11},{259:-38,27:-9},{259:-37,27:-9}]
heads=list(first)
keys=[0,-1,-2,-4,-8,-11,-15,-19,-37,-38,-40,-79,-100]
t=time.time()
for ov in BASEOV:
    print(ov,score(ov,[])[:2])
best=[]
for ov in BASEOV:
    cur=[];c=score(ov,[])[:2]
    for it in range(6):
        bm=None
        for b in heads:
            for key in keys:
                for pos in (0,99):
                    d=cur+[(b,pos,key)]
                    s=score(ov,d)[:2]
                    if s<c: c=s;bm=d
        if not bm: break
        cur=bm
        print(ov,c,cur,'%.0fs'%(time.time()-t),flush=True)
        if c[0]==0: break
