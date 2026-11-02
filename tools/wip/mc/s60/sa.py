"""sa.py TAG SECS SEED init.json: s57 SA + s59 levers (post-text substitutions):
 rf/rft  second bcp diversion on the reboot netConnect-fail edge -> ndl|dtg|rbn (depth rf)
 rp      bcp diversion right after rok's netGetInfo -> ndl (depth rp)
 E2      round-2 trace-end fakes {label:d}: bcp gotos after netDisconnect to case labels
 rx126/rx117 JUMP->JMP (RX), ebm bitmask drops eb bcp lines in clientEraseBlockI, kl drops k67l bcp (T48-ish)
FIX env pins weights; MODE env 'r2' cost = es2+1000*[R2>0]+R3W*R3. Logs sa_TAG.jsonl/best_TAG.json."""
import sys,os,json,random,time,math
D=os.path.dirname(os.path.abspath(__file__)); import importlib.util as U
_sp=U.spec_from_file_location('sa57',os.path.join(D,'..','s57','sa.py')); S=U.module_from_spec(_sp); _sp.loader.exec_module(S)
import lev,es2
FIX={}
for kv in filter(None,os.environ.get('FIX','').split(',')):
    k,v=kv.split('='); FIX[k]=int(v)
def cond(d,o): return ' && '.join('__builtin_constant_p(mode + %d)'%(o+k) for k in range(d))
EBL=['if (__builtin_constant_p(block + 90)) goto eerase;','if (__builtin_constant_p(block + 310)) goto efail;',
     'if (__builtin_constant_p(block + 91) == 3) goto eout;','if (__builtin_constant_p(block + 110)) goto eout;']
def text(st):
    s=S.text(st)
    if st.get('rf'):
        a='			} else\n				goto fail;\n		} else\n			{ AT(u2)'; assert s.count(a)==1
        t=st.get('rft','ndl')
        if t=='rbn': s=s.replace('	dtg: if (E(reboot))\n		netReboot','	dtg: if (E(reboot))\n		rbn: netReboot',1)
        s=s.replace(a,a.replace('goto fail;','{ if (%s) goto %s; goto fail; }'%(cond(st['rf'],600),t)),1)
    if st.get('d2'):
        t=st.get('d2t','ndl')
        if t=='rbn' and 'rbn: netReboot' not in s: s=s.replace('	dtg: if (E(reboot))\n		netReboot','	dtg: if (E(reboot))\n		rbn: netReboot',1)
        a='		if (reboot) {\n			if (netConnect'; assert s.count(a)==1,'d2'
        pos=st.get('d2p',0)
        if pos==0: s=s.replace(a,'		if (%s) goto %s;\n'%(cond(st['d2'],640),t)+a,1)
        else: s=s.replace(a,a.replace('if (reboot) {','if (reboot) { if (%s) goto %s;'%(cond(st['d2'],640),t)),1)
    if st.get('rE'):
        a='		if (reboot) {\n			if (netConnect(ip)) {'; assert s.count(a)==1,'rE'
        s=s.replace(a,a.replace('if (netConnect(ip))',['','if (E(netConnect(ip)))','if (__builtin_expect(netConnect(ip), 0))','if (__builtin_expect_with_probability(netConnect(ip),1,0.9))'][st['rE']]),1)
    if st.get('rp'):
        a='rok: __attribute__((cold));\n				cinfo = netGetInfo();'; assert s.count(a)==1,'rp'
        s=s.replace(a,a.replace('netGetInfo();','netGetInfo(); if (%s) goto ndl;'%cond(st['rp'],620)),1)
    g=''.join('if (%s) goto %s; '%(cond(d,700+10*i),l) for i,(l,d) in enumerate(sorted(st.get('E2',{}).items())) if d)
    if g:
        a='	ndl: netDisconnect();\n'; assert s.count(a)==1,'E2'; s=s.replace(a,a+'	'+g+'\n',1)
    if st.get('rx126'):
        a='outside system area!'+chr(92)+'n", block); JUMP(efail); }'
        i=s.find('{ eout: log_printf'); j=s.find(a,i); assert i>0 and j>0,'rx126'
        s=s[:j]+a.replace('JUMP(efail)','JMP(efail)')+s[j+len(a):]
        a=None

    if st.get('rx117'):
        assert s.count('JUMP(i0)')==1; s=s.replace('JUMP(i0)','JMP(i0)',1)
    for i,l in enumerate(EBL):
        if st.get('ebm',0)>>i&1: assert s.count(l)==1,l; s=s.replace(l,'',1)
    if st.get('kl'):
        a='if ((char *)__builtin_constant_p(i + 10) == (char *)1 && (char *)__builtin_constant_p(i + 10 + 1) == (char *)1) goto k67l;'
        assert s.count(a)==1; s=s.replace(a,'',1)
    return s
R3W=float(os.environ.get('R3W','0.5'))
def cost(st,tag):
    try: r=es2.run(text(st),tag)
    except AssertionError: raise
    except Exception: return 9999,None
    if r is None or not isinstance(r.get('per2'),dict): return 9999,None
    p=r['per2']; return r['es2']+1000*(p.get(2,0)>0)+R3W*p.get(3,0),r
def fix(n):
    w=n.setdefault('w',{})
    for k,v in FIX.items():
        if v: w[k]=v
        else: w.pop(k,None)
    return n
CL=['c12','c3','c1','t4','t5','c8','c2','c9','c10','c11','c7','cdef','p0','i0','hdd4','hdd5','u2','s5']
EN=os.environ.get('LEV','rf,rp,E2,rx,eb,kl').split(',')
def mut(s):
    n=json.loads(json.dumps(s)); k=random.random()
    if k<0.3:
        c=random.choice(EN)
        if c=='rf':
            if random.random()<0.3: n['rft']=random.choice(['ndl','dtg','rbn'])
            else: n['rf']=min(8,max(0,n.get('rf',0)+random.choice([-1,1])))
        elif c=='rp': n['rp']=min(8,max(0,n.get('rp',0)+random.choice([-1,1])))
        elif c=='E2':
            d=n.setdefault('E2',{}); l=random.choice(CL); v=d.get(l,0)+random.choice([-1,1])
            if v<=0 or v>6: d.pop(l,None)
            else: d[l]=v
        elif c=='rx': x=random.choice(['rx126','rx117']); n[x]=1-n.get(x,0)
        elif c=='eb': n['ebm']=n.get('ebm',0)^(1<<random.randrange(4))
        elif c=='kl': n['kl']=1-n.get('kl',0)
        return fix(n)
    m=S.mut(s)
    return m and fix(m)
if __name__=='__main__':
    tag,secs,seed=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]); random.seed(seed)
    a=sys.argv[4]; st=fix(json.load(open(a)) if os.path.exists(a) else json.loads(a))
    log=open(os.path.join(D,'sa_%s.jsonl'%tag),'a')
    c,r=cost(st,tag); best=c; T0=float(os.environ.get('T0','6')); t0=time.time(); it=0
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
