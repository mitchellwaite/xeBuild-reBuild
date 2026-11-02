# cl.py BASE SEED N : climb over bcp-conjunct add/del levers (dead gotos only); cost f2 + 2*orderdist
import sys,re,random,subprocess,os
sys.path.insert(0,'../s104'); import srch
base,seed,N=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); random.seed(seed)
L=open(base).read().split('\n')
grp=re.compile(r'if \(((?:\(char \*\))?__builtin_constant_p\((\w+) \+ (\d+)\)(?: == \(char \*\)1)?(?: && (?:\(char \*\))?__builtin_constant_p\([\w +]+\)(?: == \(char \*\)1)?)*)\) goto \w+;')
lev=[]
for i,l in enumerate(L):
    for m in grp.finditer(l):
        lev.append(('add',i,m.start(1)))
        if ' && ' in m.group(1): lev.append(('del',i,m.start(1)))
print(len(lev),'levers',flush=True)
def build(S,name):
    o=list(L); by={}
    for k,ln,p in S: by.setdefault(ln,[]).append((p,k))
    for ln,es in by.items():
        s=o[ln]
        for p,k in sorted(es,reverse=True):
            m=grp.match(s,p-4); g=m.group(1); x=m.group(2)
            if k=='add': g=g+' && __builtin_constant_p(%s + %d)'%(x,int(m.group(3))+987000)
            else: g=g[:g.rfind(' && ')]
            s=s[:m.start(1)]+g+s[m.end(1):]
        o[ln]=s
    open(name+'.c','w',newline='\n').write('\n'.join(o))
def ev(name):
    r=subprocess.run(['sh','../s104/run.sh',name+'.c'],capture_output=True,text=True).stdout.strip().split('\n')[-1]
    m=re.search(r'f2=(\d+) real (.*)',r)
    if not m: return 9999,r
    o=list(map(int,m.group(2).split()))
    return int(m.group(1))+0*srch.dist(o),r
nm=os.path.abspath("c2/cl_%d"%seed); cur=set(); build(cur,nm); best,r=ev(nm); print('start',best,r,flush=True)
log=open('c2/cl_%d.log'%seed,'a')
for it in range(N):
    S=set(cur)
    for _ in range(random.choice((1,1,2))):
        x=random.choice(lev)
        S={y for y in S if not (y[1]==x[1] and y[2]==x[2])} if x not in S else S
        S^={x}
    build(S,nm); v,r=ev(nm); print(it,v,r,sorted(S),file=log,flush=True)
    if v<=best:
        if v<best: print('NEW',it,v,r,flush=True); build(S,os.path.abspath('c2/clb_%d'%seed)); open('c2/clb_%d.set'%seed,'w').write(repr(sorted(S)))
        best=v; cur=S
print('best',best,sorted(cur))
