import sys,itertools,difflib,time,random
sys.path.insert(0,'../s86'); import r4sim
pre,g,first=r4sim.load(sys.argv[1])
import os
T=[int(x) for x in os.environ.get("TT","49,112,115,103,55,126,125,61,33,29,67,127,130,117,35,42,53,77,79").split(",")]
W=set(T)
def win(o):
    return [b for b in o if b in W]
def dist(o):
    w=win(o); sm=difflib.SequenceMatcher(None,w,T,autojunk=False)
    return len(T)-sum(b.size for b in sm.get_matching_blocks())
# current keys
K={}
for b,es in g.items():
    for e in es:
        if e[0]=='ins': K.setdefault(e[2],set()).add(e[3])
        if e[0]=='chg': K.setdefault(e[1],set()).add(e[2])
for e in pre:
    if e[0]=='ins': K.setdefault(e[2],set()).add(e[3])
    if e[0]=='push': K.setdefault(e[1],set()).add(e[2])
print({b:sorted(K.get(b,[])) for b in T})
base=r4sim.sim(pre,g,{}); print('base',dist(base),win(base))
B=[b for b in T]; KS=range(-8,1)
def run(n,blocks):
    hits=[];best=[]
    for bs in itertools.combinations(blocks,n):
        for ks in itertools.product(KS,repeat=n):
            ov=dict(zip(bs,ks))
            try:o=r4sim.sim(pre,g,ov)
            except Exception: continue
            d=dist(o); best.append((d,ov))
    best.sort(key=lambda x:x[0]); return best
mode=sys.argv[2]
if mode in('1','2'):
    r=run(int(mode),B)
    for d,ov in r[:25]: print(d,ov)
    print('hits',sum(1 for d,_ in r if d==0))
