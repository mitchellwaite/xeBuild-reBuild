# r4sim variant: after popping trigger block T, change key of listed blocks (in order) to prio
import sys, r4sim
from r4sim import load
import fibsim
pre,g,first=load(sys.argv[1])
trig=int(sys.argv[2]); L=[int(x) for x in sys.argv[3].split(',')]
ov=dict((int(a),int(b)) for a,b in (x.split('=') for x in sys.argv[4:]))
# inject chg events at end of trig group; prio blocks chain: each subsequent one made prio after previous pops
g=dict(g)
g[trig]=list(g.get(trig,[]))+[('chg',L[0],-1000100)]
for a,b in zip(L,L[1:]): g[a]=list(g.get(a,[]))+[('chg',b,-1000100)]
o=r4sim.sim(pre,g,ov)
T=[145,49,125,121,107,55,139,138,61,33,29,68,140,127,143,35,42,53,78,80,74]
pos={b:i for i,b in enumerate(T)}; q=[pos[b] for b in o if b in pos]
print(sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j]), ' '.join(str(b) for b in o if b in pos))
