import r4sim, itertools, sys, random
exec(open('wm.py').read().split("res=[]")[0].replace("print([pre[i] for i in mov])",""))
blocks=T[4:]
KEY={b:0 for b in blocks}
pe=[e for e in edits if e[0]=='pre']
xe=[]
for b in blocks:
    for x in first:
        if first.index(x)>=first.index(b): break
        if True:
          for where in (0,99):
            for k in sorted(set([KEY[b],KEY[b]-1,KEY[b]+1])):
                xe.append(('x',x,b,k,where))
ke=[('k',b,k) for b in blocks for k in range(-4,2) if k!=KEY[b]]
alle=pe+xe+ke
def run(S):
    p,gg=pre,dict(g); ov={}
    for ed in S:
        if ed[0]=='k': ov[ed[1]]=ed[2]
        elif ed[0]=='x':
            _,x,b,k,w=ed; l=list(gg[x]); l.insert(min(w,len(l)),('ins','this',b,k)); gg[x]=l
        else: p,gg=apply(ed,p,gg)
    return r4sim.sim(p,gg,ov)
def desc(ed):
    if ed[0]=='k': return 'key %d=%d'%(ed[1],ed[2])
    if ed[0]=='x': return 'extra ins %d(k%d) by %d@%s'%(ed[2],ed[3],ed[1],ed[4])
    return 'pre %s->before %s'%(pre[ed[1]],pre[ed[2]] if ed[2]<len(pre) else 'end')
random.seed(int(sys.argv[2]))
found={}
W=float(sys.argv[4]) if len(sys.argv)>4 else 0.3
for trial in range(int(sys.argv[3])):
    S=[]; sc=score(run(S))
    for it in range(400):
        T2=list(S); r=random.random()
        if r<0.6 or not T2: T2.append(random.choice(alle))
        elif r<0.8: T2.pop(random.randrange(len(T2)))
        else: T2[random.randrange(len(T2))]=random.choice(alle)
        try: s=score(run(T2))
        except Exception: continue
        if s+W*len(T2) <= sc+W*len(S): S,sc=T2,s
        if sc==0: break
    for ed in list(S):
        t=[x for x in S if x!=ed]
        try:
            if score(run(t))<=sc: S=t
        except Exception: pass
    k=tuple(sorted(map(desc,S)))
    if sc<=3 and k not in found: found[k]=sc; print(sc,len(S),' ; '.join(k),flush=True)
