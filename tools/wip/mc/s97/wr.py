import r4sim, itertools, sys, random
exec(open('wm.py').read().split("res=[]")[0].replace("print([pre[i] for i in mov])",""))
blocks=[29,33,107,55,139,138,61,68,53,42,35,140,127,145,78,80,74]
kedits=[('k',b,k) for b in blocks for k in range(-4,2)]
alle=edits+kedits
def run(S):
    p,gg=pre,g; ov={}
    for ed in S:
        if ed[0]=='k': ov[ed[1]]=ed[2]
        else: p,gg=apply(ed,p,gg)
    return r4sim.sim(p,gg,ov)
def desc(ed):
    if ed[0]=='k': return 'key %d=%d'%(ed[1],ed[2])
    if ed[0]=='pre': return 'pre %s->before %s'%(pre[ed[1]],pre[ed[2]] if ed[2]<len(pre) else 'end')
    return 'ins %s from %s to %s@%s'%(g[ed[1]][ed[2]],ed[1],ed[3],ed[4])
random.seed(int(sys.argv[2]))
found={}
for trial in range(int(sys.argv[3])):
    S=[]; sc=score(run(S))
    for it in range(300):
        T2=list(S)
        r=random.random()
        if r<0.6 or not T2: T2.append(random.choice(alle))
        elif r<0.8: T2.pop(random.randrange(len(T2)))
        else: T2[random.randrange(len(T2))]=random.choice(alle)
        try: s=score(run(T2))
        except Exception: continue
        if s+0.3*len(T2) <= sc+0.3*len(S): S,sc=T2,s
        if sc==0: break
    if sc<=1:
        # minimize
        for ed in list(S):
            t=[x for x in S if x!=ed]
            try:
                if score(run(t))<=sc: S=t
            except Exception: pass
        k=tuple(sorted(map(desc,S)))
        if k not in found: found[k]=sc; print(sc,len(S),' ; '.join(k),flush=True)
