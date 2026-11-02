import sys,r4sim,itertools
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
grp=int(sys.argv[2])
ins=[e for e in g[grp] if e[0]=='ins']; rest=[e for e in g[grp] if e[0]!='ins']
for perm in itertools.permutations(ins):
  for keys in itertools.product(*[[e[3]] if e[3]!=0 else [0,-1] for e in perm]):
    pp=[('ins','this',e[2],k) for e,k in zip(perm,keys)]
    gg=dict(g); gg[grp]=rest+pp; o=r4sim.sim(pre,gg,{})
    print(inv(o),[(e[2],e[3]) for e in pp],[b for b in o if b in pos])
