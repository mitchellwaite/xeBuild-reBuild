import sys, json
from lev import L, ev, inv
import os; P=os.environ.get('P','w')
cur={k:v[0] for k,v in L.items()}
for kv in sys.argv[2:]:
    k,v=kv.split('='); cur[k]=int(v)
bc,bt=ev(cur,'x_base'); bc=(bc,inv('w_base')); n=0
log=open('climb_%s.log'%sys.argv[1],'a')
print('base',bc,bt,file=log,flush=True)
for sweep in range(int(sys.argv[1])):
    imp=False
    for k,vals in L.items():
        for v in vals:
            if v==cur[k]: continue
            c=dict(cur); c[k]=v; n+=1
            s,t=ev(c,'%s%d'%(P,n)); s=(s,inv('%s%d'%(P,n)))
            print('%s%d'%(P,n),k,v,s,t,file=log,flush=True)
            if s<bc: bc,bt,cur=s,t,c; imp=True
    if not imp: break
print('best',bc,cur,bt,file=log,flush=True)
