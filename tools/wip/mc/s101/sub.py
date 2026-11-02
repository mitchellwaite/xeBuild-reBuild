# sub.py MASK : b0 with rdbest's differing lines selected by bitmask -> s_MASK.c
import sys
a=open('b0.c').read().split('\n'); b=open('rdbest.c').read().split('\n')
d=[i for i in range(len(a)) if a[i]!=b[i]]
m=int(sys.argv[1]); o=list(a)
for k,i in enumerate(d):
    if m>>k&1: o[i]=b[i]
open('s_%d.c'%m,'w',newline='\n').write('\n'.join(o))
