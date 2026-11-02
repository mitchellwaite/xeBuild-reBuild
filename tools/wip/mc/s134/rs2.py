import sys,itertools,difflib,random,math
sys.path.insert(0,'../s86'); import r4sim
pre,g,first=r4sim.load(sys.argv[1])
T=[49,112,115,103,55,126,125,61,33,29,67,127,130,117,35,42,53,77,79]
base=r4sim.sim(pre,g,{})
i0=base.index(49); i1=base.index(79)
FT=base[:i0]+T+base[i1+1:]
assert sorted(FT)==sorted(base)
def dist(o):
    sm=difflib.SequenceMatcher(None,o,FT,autojunk=False)
    return len(FT)-sum(b.size for b in sm.get_matching_blocks())
print('base',dist(base))
KS=range(-8,1)
mode=sys.argv[2]
if mode=='3':
    BL=[103,126,125,130,117,127,33,29,77,35,42,53,79]
    res=[]
    for n in (1,2,3):
        for bs in itertools.combinations(BL,n):
            for ks in itertools.product(range(-4,1),repeat=n):
                ov=dict(zip(bs,ks))
                try:d=dist(r4sim.sim(pre,g,ov))
                except Exception: continue
                res.append((d,n,ov))
    res.sort(key=lambda x:(x[0],x[1]))
    for r in res[:15]: print(r)
    print('n',len(res),'hits',sum(1 for r in res if r[0]==0))
else:
    random.seed(int(mode)); allb=list(set(base)); best=(99,{})
    for rs in range(6):
        ov={};cur=dist(base);temp=2
        for it in range(4000):
            n=dict(ov);b=random.choice(T if random.random()<.7 else allb)
            if b in n and random.random()<.3: del n[b]
            else: n[b]=random.randint(-8,0)
            try:d=dist(r4sim.sim(pre,g,n))
            except Exception: continue
            c=d+.05*len(n);cc=cur+.05*len(ov)
            if c<=cc or random.random()<math.exp((cc-c)/temp): ov,cur=n,d
            temp=max(.05,temp*.998)
            if (d,len(n))<(best[0],len(best[1])): best=(d,dict(n))
        print(rs,best,flush=True)
