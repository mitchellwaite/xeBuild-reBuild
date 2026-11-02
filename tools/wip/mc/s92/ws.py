import r4sim, itertools, sys
pre,g,first=r4sim.load(sys.argv[1])
T=[147,49,125,121,107,55,139,138,61,33,29,68,140,127,145,35,42,53,78,80,74]
front=first[:first.index(49)+1]
pos={b:i for i,b in enumerate(T)}
def score(o):
    if o[:len(front)]!=front: return 999
    q=[pos[b] for b in o if b in pos]
    return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
blocks=[29,33,107,55,139,138,61,68,53,42,35,140,127,145,78,80,74,49,125,121]
cur={}
for b in blocks:
    for k in range(-8,2): pass
base=score(r4sim.sim(pre,g,{}))
print('base',base)
res=[]
def keyof(b):
    for e in pre+sum(g.values(),[]):
        if e[0]=='push' and e[1]==b: return e[2]
        if e[0]=='ins' and e[2]==b: return e[3]
ks={b:keyof(b) for b in blocks}
singles=[]
for b in blocks:
    for d in range(-3,4):
        if d==0: continue
        ov={b:ks[b]+d}; s=score(r4sim.sim(pre,g,ov)); singles.append((s,ov))
singles.sort(key=lambda x:x[0]); print(singles[:10])
pairs=[]
for (b1,b2) in itertools.combinations(blocks,2):
  for d1 in (-2,-1,1,2):
    for d2 in (-2,-1,1,2):
        ov={b1:ks[b1]+d1,b2:ks[b2]+d2}; s=score(r4sim.sim(pre,g,ov)); pairs.append((s,ov))
pairs.sort(key=lambda x:x[0]); print(pairs[:15])
