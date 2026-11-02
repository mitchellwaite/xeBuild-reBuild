# cl.py BASE SEED N : f2 climb over asm-volatile + bcp-conj levers
import sys,re,random,subprocess
base,seed,N=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); random.seed(seed)
L=open(base).read().split('\n')
A=' __asm__ volatile (""); '
grp=re.compile(r'if \((__builtin_constant_p\((\w+) \+ (\d+)\)(?: && __builtin_constant_p\(\w+ \+ \d+\))*)\) goto \w+;')
spans={}; lev=[]
for i,l in enumerate(L):
    for m in grp.finditer(l):
        spans.setdefault(i,[]).append((m.start(1),m.end(1)))
        lev.append(('add',i,m.start(1))); 
        if ' && ' in m.group(1): lev.append(('del',i,m.start(1)))
for l in open('p.out'):
    n,c=l.split()
    if int(c)>250: continue
    m=re.match(r'p(\d+)_(\d+)',n); ln,p=int(m.group(1))-1,int(m.group(2))
    if ln in (671,672) or any(a<=p<=b for a,b in spans.get(ln,[])): continue
    lev.append(('asm',ln,p))
print(len(lev),'levers',flush=True)
def build(S,name):
    o=list(L)
    by={}
    for k,ln,p in S: by.setdefault(ln,[]).append((p,k))
    for ln,es in by.items():
        s=o[ln]
        for p,k in sorted(es,reverse=True):
            if k=='asm': s=s[:p]+A+s[p:]
            else:
                m=grp.match(s,p-4)
                g=m.group(1); x=m.group(2)
                if k=='add': g=g+' && __builtin_constant_p(%s + %d)'%(x,int(m.group(3))+987000)
                else: g=g[:g.rfind(' && ')]
                s=s[:m.start(1)]+g+s[m.end(1):]
        o[ln]=s
    open(name+'.c','w',newline='\n').write('\n'.join(o))
def ev(name):
    c=subprocess.run(['sh','f2.sh',name+'.c'],capture_output=True,text=True).stdout.strip()
    return int(c) if c.isdigit() else 9999
import os
nm=os.path.abspath("cl_%d"%seed); cur=set(); build(cur,nm); best=ev(nm); print('start',best,flush=True)
log=open('cl_%d.log'%seed,'a')
for it in range(N):
    S=set(cur)
    for _ in range(random.choice((1,1,1,2,3))):
        x=random.choice(lev)
        # keep one edit kind per conj group
        S={y for y in S if not (y[0]!='asm' and y[1]==x[1] and y[2]==x[2])} if x not in S else S
        S^={x}
    build(S,nm); v=ev(nm); print(it,v,sorted(S),file=log,flush=True)
    if v<=best:
        if v<best: print('NEW',it,v,flush=True); build(S,os.path.abspath('clb_%d'%seed)); open('clb_%d.set'%seed,'w').write(repr(sorted(S)))
        best=v; cur=S
print('best',best,sorted(cur))
