"""ds6.py TAG 'ov' TL WIDTH: beam over dummy pushes (r3,r4) and early insertions of real heads (r4 groups, r3 pushes)"""
import sys,os,time,random
import nm,r4sim
TAG=sys.argv[1]
OV=eval(sys.argv[2]) if len(sys.argv)>2 else {}
TL=float(sys.argv[3]); W=int(sys.argv[4])
pre,g,first=r4sim.load('../../../../build/v/aio_p1/%s/aio.bbro'%TAG)
k=first.index(74)
TARGET=first[:k]+nm.REF4
TS=set(TARGET); idx={h:i for i,h in enumerate(TARGET)}
ir3=[i for i,e in enumerate(pre) if e==('round',3)][0]
r3gets=[(i,e[1]) for i,e in enumerate(pre) if i>ir3 and e[0]=='get']
keyof={}
for e in pre:
    if e[0]=='push': keyof[e[1]]=e[2]
    if e[0]=='ins': keyof[e[2]]=e[3]
for b,v in g.items():
    for e in v:
        if e[0]=='ins': keyof[e[2]]=e[3]
def score(dums,ov=OV,full=False):
    g2={b:list(v) for b,v in g.items()}; p2=pre
    n=0; ins=[]
    for d in dums:
        n+=1
        if d[0]=='r4':
            l=g2.setdefault(d[1],[]); l.insert(min(d[2],len(l)),('ins','this',9000+n,d[3]))
        elif d[0]=='r3':
            ins.append((d[1],('push',9000+n,d[2])))
        elif d[0]=='ie':
            l=g2.setdefault(d[1],[]); l.insert(0,('ins','this',d[2],keyof.get(d[2],0)))
    if ins:
        p2=list(pre)
        for i,e in sorted(ins,key=lambda x:-x[0]): p2.insert(i+1,e)
    o=r4sim.sim(p2,g2,ov)
    s=[h for h in o if h in TS]
    if full: return s
    v=[idx.get(h,0) for h in s]
    return sum(1 for i in range(len(v)) for j in range(i+1,len(v)) if v[i]>v[j])
keys=[0,-4,-8,-19,-37,-38,-200]
moves=[('r4',b,p,key) for b in first for p in (0,99) for key in keys]+[('r3',i,key) for i,b in r3gets for key in keys]
hs=[h for h in first]
def grp(h):
    n=nm.N.get(h,'')
    if ':' in n and n.split(':')[1] in ('O','P','PL','I','G','GL','W','.','S'): return n.split(':')[0]
    return 'caller'
moves+=[('ie',b,h) for b in first for h in hs if b!=h and first.index(b)<first.index(h) and grp(b)==grp(h)]
if os.environ.get('NOIE'): moves=[m for m in moves if m[0]!='ie']

random.seed(int(os.environ.get('SEED','1')))
print(len(moves),'base',score([]),flush=True)
t=time.time()
beam=[([],score([]))]
seen=set()
best=(999,None)
depth=0
while time.time()-t<TL and depth<8:
    cand=[]
    for ds,_ in beam[:W]:
        ms=list(moves); random.shuffle(ms)
        for m in ms[:int(os.environ.get('MM','700'))]:
            d=ds+[m]; f=frozenset(d)
            if f in seen: continue
            seen.add(f); cand.append((score(d),d))
            if time.time()-t>TL: break
    if not cand: break
    cand.sort(key=lambda x:(x[0],len(x[1])))
    beam=[(d,s) for s,d in cand[:W*3]]
    if cand[0][0]<best[0]: best=cand[0]
    print(depth,cand[0],'%.0fs'%(time.time()-t),flush=True)
    depth+=1
    if best[0]==0: break
print('BEST',best)
