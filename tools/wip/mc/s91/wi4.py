import sys,r4sim,random
from tmap import target
n=sys.argv[1]; pre,g,first=r4sim.load('d/%s/mc.bbro'%n); T,m=target(n+'.c','d/%s/order.txt'%n)
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
bs=[b for b in T if b not in (147,148,49)]
random.seed(int(sys.argv[2])); best={}
for it in range(int(sys.argv[3])):
    ov={b:random.randint(-5,0) for b in random.sample(bs,random.randint(1,4))}
    o=r4sim.sim(pre,g,ov); v=inv(o)
    k=tuple(sorted(ov.items()))
    if v<=2: best[k]=(v,[b for b in o if b in pos])
for k,v in sorted(best.items(),key=lambda x:(x[1][0],len(x[0])))[:15]: print(v[0],k)
print(T)
