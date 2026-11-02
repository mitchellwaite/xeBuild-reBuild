"""sa.py TAG SECS SEED [init.json]: SA over rok-dispatch fake weights (+_ft) and fkbo fake split on cur.base(); cost es2."""
import sys,os,json,random,time,math
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s53'))
import cur,rkgen,es2
tag,secs,seed=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]); random.seed(seed)
KEYS=rkgen.RL+['_ft']
st={'w':{},'fk':{}}  # fk: extra fkbo fakes per fkbo real label (taken from the 21 ft fakes)
if len(sys.argv)>4: st=json.load(open(sys.argv[4]))
def text(s):
    b=cur.base2()
    if s['fk']:
        n=sum(s['fk'].values()); 
        # fkbo: one asm with 9 reals + (21-n) ft fakes; fakes to labels via second-level forward
        b=b.replace(rkgen.FOLD,fkw(s['fk']),1)
    return rkgen.mk(s['w'],base=b)
def fkw(fk):
    reals=rkgen.FL; ft=21-sum(fk.values()); labs=list(reals); body=''; outer=''; n=0
    tg=['fqE']*ft+[l for l in reals for _ in range(fk.get(l,0))]
    for j,t in enumerate(tg): labs.append('fq%d'%j); body+='fq%d: goto ofq%d; '%(j,j); outer+='ofq%d: goto %s; '%(j,t)
    return 'fkbo: { struct {} fqo; { struct {} fqv; __asm__ ("" :: "X"(&fqo), "X"(&fqv)); __asm__ goto ("" :::: %s); goto fqn; %s} fqn: ; goto fqE; %s} fqE: ;'%(', '.join(labs),body,outer)
def cost(s):
    r=es2.run(text(s),tag)
    if r is None: return 9999,None
    return r['es2']+3*r['per2'].get(2,0)+r['per2'].get(3,0),r
log=open('sa_%s.jsonl'%tag,'a')
c,r=cost(st); best=(c,json.dumps(st)); T0=6; t0=time.time(); it=0
print('init',c,r and r['per2'],flush=True)
while time.time()-t0<secs:
    it+=1; T=T0*(1-(time.time()-t0)/secs)+0.3
    n=json.loads(json.dumps(st))
    if random.random()<0.8:
        k=random.choice(KEYS); n['w'][k]=max(0,n['w'].get(k,0)+random.choice([-2,-1,1,1,2,3]))
        if n['w'][k]==0: del n['w'][k]
    else:
        k=random.choice(rkgen.FL); v=max(0,n['fk'].get(k,0)+random.choice([-1,1]))
        if v: n['fk'][k]=v
        else: n['fk'].pop(k,None)
        if sum(n['fk'].values())>21: continue
    if sum(n['w'].values())+16>58: continue
    cn,rn=cost(n)
    if rn is None: continue
    log.write(json.dumps({'c':cn,'es2':rn['es2'],'per2':rn['per2'],'ev':rn['score'],'st':n})+'\n'); log.flush()
    if cn<=c or random.random()<math.exp((c-cn)/T):
        st,c=n,cn
        if c<best[0]: best=(c,json.dumps(st)); print(it,'best',c,rn['es2'],rn['per2'],rn['score'],json.dumps(st),flush=True)
print('done',best)
