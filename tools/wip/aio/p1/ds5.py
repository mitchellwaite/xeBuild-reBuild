"""ds5.py TAG: remove r4 prefix heads from heap (as if in r3 in the natural build): which subsets give low inv"""
import sys,os,itertools
import nm,r4sim
TAG=sys.argv[1]
pre,g,first=r4sim.load('../../../../build/v/aio_p1/%s/aio.bbro'%TAG)
k=first.index(74)
TARGET=first[:k]+nm.REF4
PF=first[:k]
TS=set(TARGET); idx={h:i for i,h in enumerate(TARGET)}
XZ=nm.XZ
def score(rem,ov):
    p2=[e for e in pre if not ((e[0]=='push' and e[1] in rem) or (e[0]=='ins' and e[2] in rem) or (e[0]=='chg' and e[1] in rem))]
    o=r4sim.sim(p2,g,ov)
    s=[h for h in o if h in TS and h not in rem]
    t=[h for h in TARGET if h not in rem]
    id2={h:i for i,h in enumerate(t)}
    v=[id2[h] for h in s]
    return sum(1 for i in range(len(v)) for j in range(i+1,len(v)) if v[i]>v[j])
res=[]
for ov in [{XZ:-37},{XZ:-38}]:
  for n in range(0,5):
    for rem in itertools.combinations(PF,n):
        res.append((score(set(rem),ov),ov[XZ],rem))
res.sort(key=lambda x:x[0])
for r in res[:15]: print(r)
