"""ds9.py TAG 'ov' 'dummies' TL SEED: annealing around a dummy set (keys, positions, heads, add/remove) with sim3"""
import sys,os,time,random,math
import nm,sim3
TAG=sys.argv[1]; OV=eval(sys.argv[2]); D0=eval(sys.argv[3]); TL=float(sys.argv[4]); random.seed(int(sys.argv[5]))
pre,g3,f3,g4,f4=sim3.load('../../../../build/v/aio_p1/%s/aio.bbro'%TAG)
k=f4.index(74)
TARGET=f4[:k]+nm.REF4
idx={h:i for i,h in enumerate(TARGET)}
U=set(77+5*i for i in range(11))
F3=[b for b in f3 if b not in U]
def score(ds,ov=OV):
    G3={b:list(v) for b,v in g3.items()}; G4={b:list(v) for b,v in g4.items()}
    n=0
    for d in ds:
        n+=1; id_=9000+n
        if d[0]=='r3':
            l=G3.setdefault(d[1],[])
            l.insert(min(d[2],len(l)),('push',id_,d[3]) if d[3]>=-89 else ('ins','this',id_,d[3]))
        else:
            l=G4.setdefault(d[1],[]); l.insert(min(d[2],len(l)),('ins','this',id_,d[3]))
    o3,o4=sim3.sim(pre,G3,G4,ov)
    p=0
    if [b for b in o3 if b not in U and b<9000]!=F3: p=100
    s=[h for h in o4 if h in idx]
    v=[idx[h] for h in s]
    return p+sum(1 for i in range(len(v)) for j in range(i+1,len(v)) if v[i]>v[j])
EXCL=set(eval(os.environ.get('EXCL','[]')))
f3=[b for b in f3 if b not in EXCL]
f4x=[b for b in f4 if b not in EXCL]
K=[0,-1,-2,-3,-4,-5,-6,-8,-9,-10,-12,-15,-19,-20,-25,-30,-37,-38,-40,-50]
def rnd():
    if random.random()<.15: return ('r3',random.choice(f3),random.choice([0,99]),random.choice(K+[-95,-132]))
    return ('r4',random.choice(f4x),random.choice([0,99]),random.choice(K))
cur=list(D0); c=score(cur); best=(c,list(cur)); t=time.time()
print('start',c,flush=True)
n=0
while time.time()-t<TL and best[0]>0:
    d=list(cur); r=random.random()
    if r<.5 and d:
        i=random.randrange(len(d)); x=list(d[i])
        if random.random()<.6: x[3]=random.choice(K)
        elif random.random()<.5: x[2]=random.choice([0,99])
        else: x=list(rnd())
        d[i]=tuple(x)
    elif r<.75 and len(d)<int(os.environ.get('MAXD','7')): d.append(rnd())
    elif d: d.pop(random.randrange(len(d)))
    e=score(d); n+=1
    cost=lambda s,l:s+0.15*l
    T=max(.05,.6*(1-(time.time()-t)/TL))
    if cost(e,len(d))<=cost(c,len(cur)) or random.random()<math.exp(-(cost(e,len(d))-cost(c,len(cur)))/T):
        cur,c=d,e
        if (e,len(d))<(best[0],len(best[1])):
            best=(e,list(d)); print(best,'%.0fs'%(time.time()-t),flush=True)
print('END',n,best)
