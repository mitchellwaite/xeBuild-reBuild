"""sa.py TAG SECS SEED [init.json]: s57 SA + mutations of dd/dt (tree-only bcp depth) and npre<=14;
FIX env 'i0=0,p0=0,hdd4=2' pins weights (task 2). Logs sa_TAG.jsonl / best_TAG.json here."""
import sys,os,json,random,time,math
D=os.path.dirname(os.path.abspath(__file__)); import importlib.util as U
_sp=U.spec_from_file_location('sa57',os.path.join(D,'..','s57','sa.py')); S=U.module_from_spec(_sp); _sp.loader.exec_module(S)
FIX={}
for kv in filter(None,os.environ.get('FIX','').split(',')):
    k,v=kv.split('='); FIX[k]=int(v)
def fix(n):
    w=n.setdefault('w',{})
    for k,v in FIX.items():
        if v: w[k]=v
        else: w.pop(k,None)
    return n
def mut(s):
    if random.random()<0.25:
        n=json.loads(json.dumps(s)); k=random.choice(['dd','dt','npre'])
        lo,hi,df={'dd':(1,8,4),'dt':(1,8,1),'npre':(0,14,3)}[k]
        n[k]=min(hi,max(lo,n.get(k,df)+random.choice([-1,1])))
        return fix(n)
    n=S.mut(s)
    return n and fix(n)
if __name__=='__main__':
    tag,secs,seed=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]); random.seed(seed)
    st=fix(json.load(open(sys.argv[4])))
    log=open(os.path.join(D,'sa_%s.jsonl'%tag),'a')
    c,r=S.cost(st,tag); best=c; T0=float(os.environ.get('T0','6')); t0=time.time(); it=0
    print('init',c,r and r['per2'],flush=True)
    while time.time()-t0<secs:
        n=mut(st)
        if n is None: continue
        it+=1; T=T0*(1-(time.time()-t0)/secs)+0.3
        cn,rn=S.cost(n,tag)
        if rn is None: continue
        log.write(json.dumps({'c':cn,'es2':rn['es2'],'per2':rn['per2'],'ev':rn['score'],'st':n})+'\n'); log.flush()
        if cn<=c or random.random()<math.exp((c-cn)/T):
            st,c=n,cn
            if c<best: best=c; print(it,'best',c,rn['es2'],rn['per2'],rn['score'],json.dumps(st),flush=True); open(os.path.join(D,'best_%s.json'%tag),'w').write(json.dumps(st))
    print('done',it,best,flush=True)
