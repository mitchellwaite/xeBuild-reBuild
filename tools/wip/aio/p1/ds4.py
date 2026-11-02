"""ds4.py TAG 'ov': dummies in r3 (push after get of r3 trace head) and r4 (ins in group); beam"""
import sys,os,time,random
import nm,r4sim
TAG=sys.argv[1]
OV=eval(sys.argv[2]) if len(sys.argv)>2 else {}
pre,g,first=r4sim.load('../../../../build/v/aio_p1/%s/aio.bbro'%TAG)
k=first.index(74)
TARGET=first[:k]+nm.REF4
TS=set(TARGET); idx={h:i for i,h in enumerate(TARGET)}
# r3 get positions
ir3=[i for i,e in enumerate(pre) if e==('round',3)][0]
r3gets=[(i,e[1]) for i,e in enumerate(pre) if i>ir3 and e[0]=='get']
def score(dums,ov=OV):
    g2=None; p2=pre
    n=0
    ins=[]
    for d in dums:
        n+=1
        if d[0]=='r4':
            if g2 is None: g2={b:list(v) for b,v in g.items()}
            l=g2.setdefault(d[1],[]); l.insert(min(d[2],len(l)),('ins','this',9000+n,d[3]))
        else:
            ins.append((d[1],('push',9000+n,d[2])))
    if ins:
        p2=list(pre)
        for i,e in sorted(ins,key=lambda x:-x[0]): p2.insert(i+1,e)
    o=r4sim.sim(p2,g2 if g2 is not None else g,ov)
    s=[h for h in o if h in TS]
    v=[idx[h] for h in s]
    inv=sum(1 for i in range(len(v)) for j in range(i+1,len(v)) if v[i]>v[j])
    return inv
keys=[0,-1,-4,-8,-10,-19,-30,-37,-38,-57,-76,-200]
moves=[('r4',b,p,key) for b in first for p in (0,99) for key in keys]+[('r3',i,key) for i,b in r3gets for key in keys]
print(len(moves),'base',score([]),flush=True)
t=time.time()
beam=[([],score([]))]
seen=set()
for depth in range(6):
    cand=[]
    for ds,_ in beam[:12]:
        for m in moves:
            d=ds+[m]
            f=frozenset(d)
            if f in seen: continue
            seen.add(f)
            cand.append((score(d),d))
            if time.time()-t>float(os.environ.get('TL','100')): break
    cand.sort(key=lambda x:x[0])
    beam=[(d,s) for s,d in cand[:40]]
    print(depth,[ (s) for d,s in beam[:5]],beam[0],'%.0fs'%(time.time()-t),flush=True)
    if time.time()-t>float(os.environ.get('TL','100')) or beam[0][1]==0: break
