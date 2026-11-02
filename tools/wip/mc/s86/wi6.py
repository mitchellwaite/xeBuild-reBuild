import sys,r4sim,itertools
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
mv=[int(x) for x in sys.argv[2].split(',')]
gg={k:[e for e in v if not(e[0]=='ins' and e[2] in mv)] for k,v in g.items()}
pushes=[i for i,e in enumerate(pre) if e[0]=='push']
for perm in itertools.permutations(mv):
  for at in range(pushes[-8],len(pre)+1):
    p=list(pre); p[at:at]=[('push',b,0) for b in perm]
    try:o=r4sim.sim(p,gg,{})
    except Exception as e: continue
    print(inv(o),perm,at-len(pre),[b for b in o if b in pos])
