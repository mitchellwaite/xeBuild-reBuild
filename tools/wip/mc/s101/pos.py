# pos.py BASE PREFIX LINES... : insert asm volatile after each ';','{','}' and at line start in given lines
import sys
b=open(sys.argv[1]).read().split('\n'); pre=sys.argv[2]
A=' __asm__ volatile (""); '
for ln in map(int,sys.argv[3:]):
    t=b[ln-1]; ps=[len(t)-len(t.lstrip())]+[i+1 for i,c in enumerate(t) if c in ';{}' and i<400]
    for p in sorted(set(ps)):
        o=list(b); o[ln-1]=t[:p]+A+t[p:]
        n='%s%d_%d'%(pre,ln,p); open(n+'.c','w',newline='\n').write('\n'.join(o)); print(n)
