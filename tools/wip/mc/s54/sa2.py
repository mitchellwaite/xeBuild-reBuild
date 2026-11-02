"""sa2.py TAG SECS SEED [init.json]: SA over lev.py levers; cost es2 + 3*R2 + R3."""
import sys,os,json,random,time,math
D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D); sys.path.insert(0,os.path.join(D,'..','s53'))
import lev,rkgen,es2
tag,secs,seed=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]); random.seed(seed)
st={}
if len(sys.argv)>4:
    a=sys.argv[4]; st=json.load(open(a)) if os.path.exists(a) else json.loads(a)
RW=float(os.environ.get('RW','3'))
def cost(s):
    try: r=es2.run(lev.text(s),tag)
    except Exception: return 9999,None
    if r is None: return 9999,None
    return r['es2']+RW*r['per2'].get(2,0)+r['per2'].get(3,0),r
def mut(s):
    n=json.loads(json.dumps(s)); k=random.random()
    if k<0.35:
        d=n.setdefault('w',{}); l=random.choice(rkgen.RL+['_ft']); d[l]=max(0,d.get(l,0)+random.choice([-2,-1,1,1,2]))
        if not d[l]: del d[l]
        if sum(d.values())>14: return None
    elif k<0.45:
        d=n.setdefault('fk',{}); l=random.choice(rkgen.FL); d[l]=max(0,d.get(l,0)+random.choice([-1,1]))
        if not d[l]: del d[l]
        if sum(d.values())>21: return None
    elif k<0.7:
        d=n.setdefault('B',{}); l=random.choice(lev.LAB); v=d.get(l,0)+random.choice([-1,1])
        if v<=0 or v>6: d.pop(l,None)
        else: d[l]=v
    elif k<0.9:
        d=n.setdefault('X',{}); l=random.choice(lev.LAB); v=d.get(l,0)+random.choice([-1,1])
        if v<=0 or v>5: d.pop(l,None)
        else: d[l]=v
    else:
        p=random.choice(['npre','dd','dt']); dv={'npre':3,'dd':4,'dt':1}[p]
        n[p]=min(6,max(1,n.get(p,dv)+random.choice([-1,1])))
    return n
log=open(os.path.join(D,'sa2_%s.jsonl'%tag),'a')
c,r=cost(st); best=(c,json.dumps(st)); T0=float(os.environ.get('T0','5')); t0=time.time(); it=0
print('init',c,r and r['per2'],flush=True)
while time.time()-t0<secs:
    it+=1; T=T0*(1-(time.time()-t0)/secs)+0.3
    n=mut(st)
    if n is None: continue
    cn,rn=cost(n)
    if rn is None: continue
    log.write(json.dumps({'c':cn,'es2':rn['es2'],'per2':rn['per2'],'ev':rn['score'],'st':n})+'\n'); log.flush()
    if cn<=c or random.random()<math.exp((c-cn)/T):
        st,c=n,cn
        if c<best[0]: best=(c,json.dumps(st)); print(it,'best',c,rn['es2'],rn['per2'],rn['score'],json.dumps(st),flush=True)
print('done',best,flush=True)
