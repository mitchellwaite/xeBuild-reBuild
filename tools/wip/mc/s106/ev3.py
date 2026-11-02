import sys, itertools
sys.path.insert(0,'../s104'); sys.path.insert(0,'../s86')
import srch, r4sim, m
pre,g,first=r4sim.load('dmp_w/mc.bbro')
def ap(p,gg,w):
    for e,p2,g2 in m.edits(p,gg):
        if e==w: return p2,g2
    raise Exception(w)
for k29,k33 in itertools.product((-3,-2,-1),(-3,-2,-1)):
  p=[('push',e[1],k29) if e==('push',29,-3) else ('push',e[1],k33) if e==('push',33,-2) else e for e in pre]
  for t in range(197,210,2):
   for k139 in (-3,-2):
    for k55 in (-3,-2):
      p2,gg=ap(p,g,('i2p',139,t,k139)); p2,gg=ap(p2,gg,('mvi',55,49,0,k55))
      o=srch.sim(p2,gg); d=srch.dist(o)
      if d<=2: print(k29,k33,t,k139,k55,d,' '.join(map(str,o)))
