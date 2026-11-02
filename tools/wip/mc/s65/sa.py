"""sa.py TAG SECS SEED init.json: s62 SA (PD+TH) + dispatch-raising levers:
POST = depth of a post-loop dead goto (argc bcp) into label dsp before switch (raises dispatch block freq,
steals from the rest of the post-loop region); LT = depth of a loop-top dead goto (i bcp) into dsp."""
import sys,os,json,random,time,math
D=os.path.dirname(os.path.abspath(__file__)); import importlib.util as U
_sp=U.spec_from_file_location('sa62',os.path.join(D,'..','s62','sa.py')); T=U.module_from_spec(_sp); _sp.loader.exec_module(T)
P=T.P; S=T.S
def cv(v,d,o): return ' && '.join('__builtin_constant_p(%s + %d)'%(v,o+k) for k in range(d))
def text(st):
    s=T.text(st); po=st.get('POST',0); lt=st.get('LT',0)
    if po or lt:
        a='switch (mode) {\n			case 1:'; assert s.count(a)==1; s=s.replace(a,'dsp: '+a)
    if po:
        a='	if (NO_MODE_ARG(mode, arg)) {\n'; assert s.count(a)==1
        s=s.replace(a,'	if (%s) goto dsp;\n'%cv('argc',po,1500)+a)
    if lt:
        a='	for (i = 0; i < argc; i++) {\n'; assert s.count(a)==1
        s=s.replace(a,a+'if (%s) goto dsp;\n'%cv('i',lt,1600))
    return s
R3W=float(os.environ.get('R3W','2'))
def cost(st,tag):
    try: r=T.es2.run(text(st),tag)
    except AssertionError: raise
    except Exception: return 9999,None
    if r is None or not isinstance(r.get('per2'),dict): return 9999,None
    p=r['per2']; return r['es2']+PEN[0]*p.get(2,0)+R3W*p.get(3,0),r
PEN=[2.0]
def fx(n,o):
    for k in ('TH','POST','LT'):
        if k in o: n[k]=o[k]
    return n
def mut(s):
    if random.random()<float(os.environ.get('PDR','0.12')):
        n=json.loads(json.dumps(s)); k=random.choice(['POST','LT']) if os.environ.get('LTON') else 'POST'
        v=n.get(k,0)+random.choice([-1,1])
        if v<=0 or v>10: v=0
        if k=='POST' and os.environ.get('PMIN'): v=max(int(os.environ['PMIN']),min(v or 99,int(os.environ.get('PMAX','10'))))
        n[k]=v; return n
    n=T.mut(s)
    if n is None: return None
    for k in ('POST','LT'):
        if k in s and k not in n: n[k]=s[k]
    if 'TH' not in n and 'TH' in s: n['TH']=s['TH']
    return n
if __name__=='__main__':
    tag,secs,seed=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]); random.seed(seed)
    a=sys.argv[4]; st0=json.load(open(a)) if os.path.exists(a) else json.loads(a)
    st=fx(S.fix(dict(st0)),st0)
    for k,v in [x.split('=') for x in sys.argv[5:]]: st[k]=int(v)
    if secs==0:
        c,r=cost(st,tag); print(c,r and {k:r.get(k) for k in ('es2','per2','score')}); sys.exit()
    log=open(os.path.join(D,'sa_%s.jsonl'%tag),'a')
    c,r=cost(st,tag); best=c; b2=9999; T0=float(os.environ.get('T0','4')); t0=time.time(); it=0
    print('init',c,r and r['es2'],r and r['per2'],flush=True)
    while time.time()-t0<secs:
        n=mut(st)
        if n is None: continue
        fr=(time.time()-t0)/secs; PEN[0]=2.0*(200**fr); it+=1; Tt=T0*(1-(time.time()-t0)/secs)+0.3
        try: cn,rn=cost(n,tag)
        except AssertionError: continue
        if rn is None: continue
        log.write(json.dumps({'c':cn,'es2':rn['es2'],'per2':rn['per2'],'ev':rn['score'],'st':n})+'\n'); log.flush()
        if rn['per2'].get(2,0)==0 and rn['es2']<b2: b2=rn['es2']; print(it,'b2',b2,rn['per2'],flush=True); open(os.path.join(D,'b2_%s.json'%tag),'w').write(json.dumps(n))
        if cn<=c or random.random()<math.exp((c-cn)/Tt):
            st,c=n,cn
            if c<best and fr>0.9: best=c; print(it,'best',c,rn['es2'],rn['per2'],rn['score'],json.dumps(st),flush=True); open(os.path.join(D,'best_%s.json'%tag),'w').write(json.dumps(st))
    print('done',it,best,flush=True)
