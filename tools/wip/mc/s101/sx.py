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
    return (hd, int(c) if c.isdigit() else 9999, int(m.group(1)) if m else 999)
nm="sx_%d"%seed; cur=set(eval(open(sys.argv[4]).read()))
log=open('sx_%d.log'%seed,'a')
for x in lev:
    if x in cur: continue
    S=cur|{x}; build(S,nm); v=ev(nm); print(x,v,file=log,flush=True)
