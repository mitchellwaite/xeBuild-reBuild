# climb.py BASE SEED N : hill-climb over zero-byte asm-volatile levers (insert positions), objective inv (then fncmp)
import sys,re,random,subprocess,os
base,seed,N=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
random.seed(seed)
s=open(base).read(); L=s.split('\n')
A=' __asm__ volatile ("");'
lev=[]
for m in re.finditer(r'AT\((\w+)\)',s):
    if m.group(1)!='l': lev.append(m.start())
off=[0]
for t in L: off.append(off[-1]+len(t)+1)
for l in open('p.out'):
    n,c=l.split(); c=int(c)
    if c in(26,9999) or c>200: continue
    m=re.match(r'p(\d+)_(\d+)',n); ln,p=int(m.group(1)),int(m.group(2))
    lev.append(off[ln-1]+p)
lev=sorted(set(lev))
print(len(lev),'levers',flush=True)
def build(S,name):
    t=s
    for p in sorted(S,reverse=True): t=t[:p]+A+' '+t[p:]
    open(name+'.c','w',newline='\n').write(t)
def ev(name):
    subprocess.run(['sh','dd.sh',name+'.c'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    o=subprocess.run(['python','inv.py',name],capture_output=True,text=True).stdout
    m=re.search(r'inv=(\d+)',o); iv=int(m.group(1)) if m else 999
    c=subprocess.run(['sh','f.sh',name+'.c'],capture_output=True,text=True).stdout.strip()
    return (int(c) if c.isdigit() else 9999, iv)
cur=set(); best=(26,5); nm='cl%d'%seed
log=open('climb%d.log'%seed,'a')
for it in range(N):
    S=set(cur)
    for _ in range(random.choice((1,1,2))):
        S^={random.choice(lev)}
    build(S,nm); v=ev(nm)
    print(it,v,sorted(lev.index(p) for p in S),file=log,flush=True)
    if v<=best:
        if v<best: print('NEW',v,sorted(S),flush=True); os.replace(nm+'.c','fbest%d_%d_%d.c'%(seed,v[0],v[1]))
        best=v; cur=S
print('best',best,sorted(lev.index(p) for p in cur))
