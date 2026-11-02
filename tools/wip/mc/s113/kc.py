# kc.py dmp : hill-climb key overrides (case blocks), with/without 141 push, min r4sim dist
import sys, random
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s111')
from wi import *
pre, g, first = r4sim.load(sys.argv[1])
B = [142,113,116,119,122,134,115,129,131,126,147,105,49,125,121,108,139,55,138,62]
def K(p,f): return -(1000000+100*p+f) if p else -f
KS = [K(p,f) for p in range(0,11) for f in range(0,16)]
best=(99,None)
random.seed(int(sys.argv[2]))
for push in [None]+[K(p,f) for p in (2,3,4,5,6) for f in (6,8,9,10,12)]:
  P = push141(pre, push) if push else pre
  ov = {}; d = srch.dist(srch.sim(P,g,ov))
  for it in range(1500):
    o2 = dict(ov); b=random.choice(B)
    if random.random()<0.2 and b in o2: del o2[b]
    else: o2[b]=random.choice(KS)
    d2 = srch.dist(srch.sim(P,g,o2))
    if d2<=d: d,ov=d2,o2
  if d<best[0]: best=(d,push,ov); print(d,push,ov,flush=True)
print('BEST',best)
