# climb3.py BASE SEED N : climb (fncmp, inv) over asm-volatile levers from p.out (line_col on b0 lines), base may add asm on other lines
import sys,re,random,subprocess,os
base,seed,N=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); random.seed(seed)
L=open(base).read().split('\n'); B0=open('b0.c').read().split('\n')
A=' __asm__ volatile (""); '
lev=[]
for l in open('p.out'):
    n,c=l.split(); c=int(c)
    if c==9999 or c>250: continue
    m=re.match(r'p(\d+)_(\d+)',n); ln,p=int(m.group(1)),int(m.group(2))
    if L[ln-1]!=B0[ln-1]: continue
    lev.append((ln,p))
print(len(lev),'levers',flush=True)
def build(S,name):
    o=list(L)
    for ln,p in sorted(S,reverse=True): o[ln-1]=o[ln-1][:p]+A+o[ln-1][p:]
    open(name+'.c','w',newline='\n').write('\n'.join(o))
def ev(name):
    c=subprocess.run(['sh','f2.sh',name+'.c'],capture_output=True,text=True).stdout.strip()
    subprocess.run(['sh','dd.sh',name+'.c'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    o=subprocess.run(['python','inv.py',name],capture_output=True,text=True).stdout
    m=re.search(r'inv=(\d+)',o)
    h=subprocess.run(['python','hs.py',name],capture_output=True,text=True).stdout
    b=open('d/b0/hs.txt').read()
    import difflib
    hd=sum(1 for x in difflib.ndiff(b.split(),h.split()) if x[:1] in '+-')
    return (int(c) if c.isdigit() else 9999, hd, int(m.group(1)) if m else 999)
nm="c6_%d"%seed; cur=set(eval(open(sys.argv[4]).read())) if len(sys.argv)>4 else set(); best=None
build(cur,nm); best=ev(nm); print('start',best,flush=True)
log=open('climb6_%d.log'%seed,'a')
for it in range(N):
    S=set(cur)
    for _ in range(random.choice((1,1,2,3))): S^={random.choice(lev)}
    build(S,nm); v=ev(nm); print(it,v,sorted(S),file=log,flush=True)
    if v<=best:
        if v<best: print('NEW',it,v,flush=True); build(S,'c6b_%d'%seed); open('c6b_%d.set'%seed,'w').write(repr(sorted(S)))
        best=v; cur=S
print('best',best,sorted(cur))
