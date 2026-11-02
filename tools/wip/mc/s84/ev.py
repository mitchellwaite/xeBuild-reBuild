import sys
sys.path.insert(0,r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip')
import fibsim
ev=fibsim.parse('d/%s/mc.bbro'%sys.argv[2])
from tmap import target; T,_=target(sys.argv[2]+".c","d/%s/order.txt"%sys.argv[2]); S=set(T)
rnd=0;last=None
for e in ev:
    if e[0]=='round': rnd=e[1]; print('R',rnd,end=' | '); continue
    if e[0]=='get': last=e[1]
    if rnd>=3 and e[0]!='visit' and any(x in S for x in e[1:] if isinstance(x,int)) : print('%s:%s'%(last,e[0][0]+','.join(map(str,e[1:]))),end=' ')
print()
