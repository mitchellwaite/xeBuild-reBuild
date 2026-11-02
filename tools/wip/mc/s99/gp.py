# gp.py BASE PFX L0 L1 : insert empty asm volatile after each ';' '{' '}' / before labels on lines L0..L1 (skip long lines)
import sys,re
base,pfx,l0,l1=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
L=open(base).read().split('\n')
A=' __asm__ volatile ("");'
k=0
for ln in range(l0-1,l1):
    t=L[ln]
    if len(t)>400 or t.strip().startswith('#') or 'case ' in t and t.strip().endswith(':') : continue
    pos=set()
    for m in re.finditer(r'[;{}]',t): pos.add(m.end())
    for m in re.finditer(r'\b(\w+):(?!:)',t):
        if m.group(1) not in('default',) : pos.add(m.start())
    # skip positions inside parentheses
    for p in sorted(pos):
        d=t[:p].count('(')-t[:p].count(')')
        if d!=0: continue
        L2=list(L); L2[ln]=t[:p]+A+t[p:]
        n='%s%03d_%d'%(pfx,ln+1,p); open(n+'.c','w',newline='\n').write('\n'.join(L2)); print(n); k+=1
