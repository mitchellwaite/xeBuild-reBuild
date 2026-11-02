"""sa.py TAG SECS SEED init.json: s62 SA (PD+TH) + LP lever: tail asm-goto back edges to dsp at
`cinfo = netGetInfo();` after fkbo (LP = {case: multiplicity}), with dsp listed first in rok's asm goto
so the DFS enters the cycle at dsp (keeps R2 = 0)."""
import sys,os,json,random,time,math,re
D=os.path.dirname(os.path.abspath(__file__)); import importlib.util as U
_sp=U.spec_from_file_location('sa62',os.path.join(D,'..','s62','sa.py')); T=U.module_from_spec(_sp); _sp.loader.exec_module(T)
S=T.S; es2=T.es2
LABS=['c1','c3','c7','c8','c9','c10','c11','c12','cdef','i0','p0','u2','s5','hdd4','hdd5']
import re
def strip(s,L):
    for l in L:
        a=s.index('rok: __attribute__'); b=s.index('fkN: ;',a); g=s[a:b]
        g=re.sub(r', %s(?=[,)])'%l,'',g); g=re.sub(r'(ork\d+: goto) %s;'%l,r'\1 rkE;',g); s=s[:a]+g+s[b:]
    return s
CASES=['1','2','3','4','5','7','8','9','10','11','12','d']
def text(st):
    s=strip(T.text(st),st.get('ST',[])); lp={k:v for k,v in st.get('LP',{}).items() if v>0}
    if not lp: return s
    i=s.index('if (NO_MODE_ARG(mode, arg)) {'); f=s.index('fkbo: {',i)
    g=s.index('cinfo = netGetInfo();',f); s=s[:g]+'dsp: '+s[g:]
    r=s.index('rok:',i); a=s.index('__asm__ goto ("" :::: ',r)+len('__asm__ goto ("" :::: '); s=s[:a]+'dsp, '+s[a:]
    j=s.index('switch (mode) {',i)
    for c,n in lp.items():
        lab='case %s:'%c if c!='d' else 'default:'
        b=s.index('break;',s.index(lab,j)); s=s[:b]+'__asm__ goto ("" :::: dsp); '*n+s[b:]
    return s
FW=float(os.environ.get('FW','0.1'))
R3W=float(os.environ.get('R3W','2'))
def cost(st,tag):
    try: r=es2.run(text(st),tag,True)
    except AssertionError: raise
    except Exception: return 9999,None
    if r is None or not isinstance(r.get('per2'),dict): return 9999,None
    p=r['per2']; f=r.get('fncmp') or 999; return f+FW*(r['es2']+R3W*p.get(3,0)),r
def keep(n,s):
    for k in ('TH','LP','ST'):
        if k in s and k not in n: n[k]=json.loads(json.dumps(s[k]))
    return n
def mut(s):
    if random.random()<float(os.environ.get('PLP','0.2')):
        n=json.loads(json.dumps(s)); lp=n.setdefault('LP',{}); c=random.choice(CASES)
        lp[c]=max(0,min(3,lp.get(c,0)+random.choice([-1,1])))
        if not lp[c]: del lp[c]
        return n
    if random.random()<float(os.environ.get('PST','0.15')):
        n=json.loads(json.dumps(s)); st=set(n.get('ST',[])); st^={random.choice(LABS)}; n['ST']=sorted(st); return n
    n=T.mut(s)
    return None if n is None else keep(n,s)
if __name__=='__main__':
    tag,secs,seed=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]); random.seed(seed)
    a=sys.argv[4]; st0=json.load(open(a)) if os.path.exists(a) else json.loads(a)
    st=keep(S.fix(dict(st0)),st0)
    if len(sys.argv)>5: st['LP']=json.loads(sys.argv[5])
    if secs==0:
        c,r=cost(st,tag); print(c,r and {k:r.get(k) for k in ('es2','per2','score','fncmp')}); sys.exit()
    log=open(os.path.join(D,'sa_%s.jsonl'%tag),'a')
    c,r=cost(st,tag); best=c; T0=float(os.environ.get('T0','4')); t0=time.time(); it=0
    print('init',c,r and r['es2'],r and r['per2'],flush=True)
    while time.time()-t0<secs:
        n=mut(st)
        if n is None: continue
        it+=1; Tt=T0*(1-(time.time()-t0)/secs)+0.3
        try: cn,rn=cost(n,tag)
        except AssertionError: continue
        if rn is None: continue
        log.write(json.dumps({'c':cn,'es2':rn['es2'],'per2':rn['per2'],'ev':rn['score'],'f':rn.get('fncmp'),'st':n})+'\n'); log.flush()
        if cn<=c or random.random()<math.exp((c-cn)/Tt):
            st,c=n,cn
            if c<best: best=c; print(it,'best',c,rn['es2'],rn['per2'],rn['score'],json.dumps(st),flush=True); open(os.path.join(D,'best_%s.json'%tag),'w').write(json.dumps(st))
    print('done',it,best,flush=True)
