"""sa.py TAG SECS SEED [init.json]: joint SA over rok weights + chunk order + cap + npre (+lev keys);
cost = es2 + 1000*[R2>0] + 0.5*R3. Log sa_TAG.jsonl."""
import sys,os,json,random,time,math
D=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(D,'..','s54')); sys.path.insert(0,os.path.join(D,'..','s53'))
import rkgen,lev,es2
EXT=['t4','t5']
def rok2(w,order=None,cap=30,real=True,pref='rk'):
    labs=list(order or rkgen.RL) if real else []
    fk=[]
    for l in list(order or rkgen.RL)+EXT+['_ft']:
        for j in range(w.get(l,0)): fk.append(l if l!='_ft' else pref+'E')
    allt=[(x,None) for x in labs]+[('%s%d'%(pref,i),t) for i,t in enumerate(fk)]
    if os.environ.get('FKFIRST'): allt=allt[len(labs):]+allt[:len(labs)]
    chunks=[allt[i:i+cap] for i in range(0,len(allt),cap)] or [[]]
    s='{ struct {} %so; '%pref; outer=''
    for ci,ch in enumerate(chunks):
        s+='{ struct {} %sv%d; __asm__ ("" :: "X"(&%so), "X"(&%sv%d)); __asm__ goto ("" :::: %s); goto %sn%d; '%(pref,ci,pref,pref,ci,', '.join(x for x,_ in ch),pref,ci)
        for x,t in ch:
            if t: s+='%s: goto o%s; '%(x,x); outer+='o%s: goto %s; '%(x,t)
        s+='} %sn%d: ; '%(pref,ci)
    return s+'goto %sE; '%pref+outer+'} %sE: ; '%pref
rkgen.rok=rok2
def text(st):
    old=rkgen.mk
    rkgen.mk=lambda ww,base=None: old(ww,order=st.get('order'),cap=st.get('cap',30),base=base)
    try: return lev.text(st)
    finally: rkgen.mk=old
R3W=float(os.environ.get('R3W','0.5'))
def cost(st,tag):
    try: r=es2.run(text(st),tag)
    except Exception: return 9999,None
    if r is None or not isinstance(r.get('per2'),dict): return 9999,None
    p=r['per2']; return r['es2']+1000*(p.get(2,0)>0)+R3W*p.get(3,0),r
def mut(s):
    n=json.loads(json.dumps(s)); k=random.random()
    if k<0.4:
        d=n.setdefault('w',{}); l=random.choice(rkgen.RL+['_ft']+EXT*3); d[l]=max(0,d.get(l,0)+random.choice([-1,1]))
        if not d[l]: del d[l]
        if sum(d.values())>40: return None
    elif k<0.6:
        o=n.get('order') or list(rkgen.RL); i,j=random.sample(range(len(o)),2); o[i],o[j]=o[j],o[i]; n['order']=o
    elif k<0.7: n['cap']=min(30,max(6,n.get('cap',30)+random.choice([-4,-2,-1,1,2,4])))
    elif k<0.82: n['npre']=min(10,max(0,n.get('npre',3)+random.choice([-1,1])))
    elif k<0.91:
        d=n.setdefault('X',{}); l=random.choice(lev.LAB); v=d.get(l,0)+random.choice([-1,1])
        if v<=0 or v>5: d.pop(l,None)
        else: d[l]=v
    else:
        d=n.setdefault('B',{}); l=random.choice(lev.LAB); v=d.get(l,0)+random.choice([-1,1])
        if v<=0 or v>6: d.pop(l,None)
        else: d[l]=v
    return n
if __name__=='__main__':
    tag,secs,seed=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]); random.seed(seed)
    st={'w':{'cdef':6,'hdd4':3,'hdd5':3,'u2':2,'c3':2,'p0':2,'c11':1}}
    if len(sys.argv)>4:
        a=sys.argv[4]; st=json.load(open(a)) if os.path.exists(a) else json.loads(a)
    log=open(os.path.join(D,'sa_%s.jsonl'%tag),'a')
    c,r=cost(st,tag); best=c; T0=float(os.environ.get('T0','6')); t0=time.time(); it=0
    print('init',c,r and r['per2'],flush=True)
    while time.time()-t0<secs:
        n=mut(st)
        if n is None: continue
        it+=1; T=T0*(1-(time.time()-t0)/secs)+0.3
        cn,rn=cost(n,tag)
        if rn is None: continue
        log.write(json.dumps({'c':cn,'es2':rn['es2'],'per2':rn['per2'],'ev':rn['score'],'st':n})+'\n'); log.flush()
        if cn<=c or random.random()<math.exp((c-cn)/T):
            st,c=n,cn
            if c<best: best=c; print(it,'best',c,rn['es2'],rn['per2'],rn['score'],json.dumps(st),flush=True); open(os.path.join(D,'best_%s.json'%tag),'w').write(json.dumps(st))
    print('done',it,best,flush=True)
