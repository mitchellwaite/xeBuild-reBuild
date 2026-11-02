"""sa.py TAG SECS SEED init.json: s60 SA + PD lever = ordered list of pre-dispatch tree-only bcp diversions
[[label, depth], ...] placed after the switch path's netGetInfo (raises one case head's freq, lowers the
uniform dispatch share). Env as s60 (R3W, FIX, T0, LEV); PDP=1 also allows 'pdp' (placement before netGetInfo).
Logs sa_TAG.jsonl / best_TAG.json here."""
import sys,os,json,random,time,math
D=os.path.dirname(os.path.abspath(__file__)); import importlib.util as U
_sp=U.spec_from_file_location('sa60',os.path.join(D,'..','s60','sa.py')); S=U.module_from_spec(_sp); _sp.loader.exec_module(S)
import es2
PDL=['c12','c3','c1','t5','t4','c8','c2','c9','c10','c11','c7','cdef','s5','s4','hdd4','hdd5','p0','p1','i0','i1']
def cond(d,o): return ' && '.join('__builtin_constant_p(mode + %d)'%(o+k) for k in range(d))
def text(st):
    s=S.text(st); pd=[x for x in st.get('PD',[]) if x[1]>0]
    if pd:
        g=''.join('if (%s) goto %s; '%(cond(d,900+10*i),l) for i,(l,d) in enumerate(pd))
        a='			cinfo = netGetInfo();\n			switch (mode) {'; assert s.count(a)==1,'PD'
        if st.get('pdp'): s=s.replace(a,'			'+g+'\n'+a,1)
        else: s=s.replace(a,'			cinfo = netGetInfo();\n			'+g+'\n			switch (mode) {',1)
    return s
R3W=float(os.environ.get('R3W','1'))
def cost(st,tag):
    try: r=es2.run(text(st),tag)
    except AssertionError: raise
    except Exception: return 9999,None
    if r is None or not isinstance(r.get('per2'),dict): return 9999,None
    p=r['per2']; return r['es2']+1000*(p.get(2,0)>0)+R3W*p.get(3,0),r
def mut(s):
    if random.random()<float(os.environ.get('PPD','0.35')):
        n=json.loads(json.dumps(s)); pd=n.setdefault('PD',[]); k=random.random()
        if k<0.3 and len(pd)<10: pd.insert(random.randint(0,len(pd)),[random.choice(PDL),random.randint(2,7)])
        elif k<0.45 and pd: pd.pop(random.randrange(len(pd)))
        elif k<0.8 and pd:
            e=random.choice(pd); e[1]=min(9,max(1,e[1]+random.choice([-1,1])))
        elif k<0.9 and len(pd)>1:
            i,j=random.sample(range(len(pd)),2); pd[i],pd[j]=pd[j],pd[i]
        elif pd: random.choice(pd)[0]=random.choice(PDL)
        elif os.environ.get('PDP'): n['pdp']=1-n.get('pdp',0)
        else: return None
        return S.fix(n)
    return S.mut(s)
if __name__=='__main__':
    tag,secs,seed=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]); random.seed(seed)
    a=sys.argv[4]; st=S.fix(json.load(open(a)) if os.path.exists(a) else json.loads(a))
    log=open(os.path.join(D,'sa_%s.jsonl'%tag),'a')
    c,r=cost(st,tag); best=c; T0=float(os.environ.get('T0','4')); t0=time.time(); it=0
    print('init',c,r and r['es2'],r and r['per2'],flush=True)
    while time.time()-t0<secs:
        n=mut(st)
        if n is None: continue
        it+=1; T=T0*(1-(time.time()-t0)/secs)+0.3
        try: cn,rn=cost(n,tag)
        except AssertionError: continue
        if rn is None: continue
        log.write(json.dumps({'c':cn,'es2':rn['es2'],'per2':rn['per2'],'ev':rn['score'],'st':n})+'\n'); log.flush()
        if cn<=c or random.random()<math.exp((c-cn)/T):
            st,c=n,cn
            if c<best: best=c; print(it,'best',c,rn['es2'],rn['per2'],rn['score'],json.dumps(st),flush=True); open(os.path.join(D,'best_%s.json'%tag),'w').write(json.dumps(st))
    print('done',it,best,flush=True)
