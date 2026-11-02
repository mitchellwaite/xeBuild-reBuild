"""sa.py TAG SECS SEED init.json: s61 SA (PD) + TH lever = list of [label,depth] jump-threading
assignments `if (bcp^depth) mode = V;` right before the switch. vrp/dom thread them to case V and
update_bb_profile_for_threading lowers ONLY that dispatch edge's prob; fab later folds bcp -> 0,
so no code remains. Gives uneven switch edge probabilities. Logs sa_TAG.jsonl / best_TAG.json."""
import sys,os,json,random,time,math
D=os.path.dirname(os.path.abspath(__file__)); import importlib.util as U
_sp=U.spec_from_file_location('sa61',os.path.join(D,'..','s61','sa.py')); P=U.module_from_spec(_sp); _sp.loader.exec_module(P)
S=P.S; es2=P.es2
VAL={'c%d'%k:k for k in range(1,13)}; VAL.update({'t4':4,'t5':5,'cdef':99})
THL=list(VAL)
def text(st):
    s=P.text(st); th=[x for x in st.get('TH',[]) if x[1]>0]
    if th:
        g=''.join('if (%s) mode = %d; '%(P.cond(d,1100+10*i),VAL[l]) for i,(l,d) in enumerate(th))
        i=s.index('switch (mode) {\n			case 1:'); s=s[:i]+g+s[i:]
    return s
R3W=float(os.environ.get('R3W','2'))
def cost(st,tag):
    try: r=es2.run(text(st),tag)
    except AssertionError: raise
    except Exception: return 9999,None
    if r is None or not isinstance(r.get('per2'),dict): return 9999,None
    p=r['per2']; return r['es2']+1000*(p.get(2,0)>0)+R3W*p.get(3,0),r
def mut(s):
    if random.random()<float(os.environ.get('PTH','0.35')):
        n=json.loads(json.dumps(s)); th=n.setdefault('TH',[]); k=random.random()
        if k<0.35 and len(th)<14: th.insert(random.randint(0,len(th)),[random.choice(THL),random.randint(2,7)])
        elif k<0.5 and th: th.pop(random.randrange(len(th)))
        elif k<0.85 and th:
            e=random.choice(th); e[1]=min(9,max(1,e[1]+random.choice([-1,1])))
        elif th: random.choice(th)[0]=random.choice(THL)
        else: return None
        return S.fix(n) if 'TH' in S.fix(n) else dict(S.fix(n),TH=th)
    return P.mut(s)
if __name__=='__main__':
    tag,secs,seed=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]); random.seed(seed)
    a=sys.argv[4]; st=json.load(open(a)) if os.path.exists(a) else json.loads(a)
    th=st.get('TH',[]); st=S.fix(st); st['TH']=th
    if secs==0:
        c,r=cost(st,tag); print(c,r and {k:r.get(k) for k in ('es2','per2','score','fncmp')}); sys.exit()
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
