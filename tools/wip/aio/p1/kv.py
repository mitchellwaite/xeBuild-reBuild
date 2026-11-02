"""kv.py TAG TL SEED: model search: key levels (dead-exit lowering) for tie groups; minimize (inv, number of changed keys)"""
import sys,os,time,random
import nm,r4sim
TAG=sys.argv[1]; TL=float(sys.argv[2]); random.seed(int(sys.argv[3]))
pre,g,first=r4sim.load('../../../../build/v/aio_p1/%s/aio.bbro'%TAG)
k=first.index(74)
TARGET=first[:k]+nm.REF4
idx={h:i for i,h in enumerate(TARGET)}
XZ=nm.XZ
GU=[94,89,124,119,114,109,84,79,104,99,129]
LV={}
for b in GU: LV[b]=[37,31,26,22]
LV[XZ]=[38,37,31]
for b in [156,166,217,176,207]: LV[b]=[19,16,13]
for b in [17,57,7,67,47,37]: LV[b]=[8,7,6]
LV[237]=[8,7,6,5]
for b in [167,177,218,208,157]: LV[b]=[4,3]
LV[229]=[11,15,16]; LV[27]=[10,9,8]
for b in [36,16,6,56,66,46]: LV[b]=[38,32]
LV[201]=[38]
base={b:v[0] for b,v in LV.items()}
base[229]=11;base[27]=10
def ev(a):
    ov={b:-v for b,v in a.items()}
    o=r4sim.sim(pre,g,ov)
    s=[h for h in o if h in idx]
    v=[idx[h] for h in s]
    inv=sum(1 for i in range(len(v)) for j in range(i+1,len(v)) if v[i]>v[j])
    ch=sum(1 for b in a if a[b]!=LV[b][0])
    return inv,ch
cur=dict(base);c=ev(cur);best=(c,dict(cur))
t=time.time();T=1.0;n=0
keys=list(LV)
while time.time()-t<TL:
    d=dict(cur)
    for _ in range(random.choice([1,1,2])):
        b=random.choice(keys); d[b]=random.choice(LV[b])
    e=ev(d);n+=1
    ec=e[0]*20+e[1]; cc=c[0]*20+c[1]
    if ec<=cc or random.random()<2.718**(-(ec-cc)/(T*8)):
        cur,c=d,e
        if e[0]*20+e[1]<best[0][0]*20+best[0][1]:
            best=(e,dict(d)); print(best[0],{b:v for b,v in d.items() if v!=LV[b][0]},'%.0fs'%(time.time()-t),flush=True)
    T=max(.05,1-(time.time()-t)/TL)
print('END',n,best[0],{b:v for b,v in best[1].items() if v!=LV[b][0]})
