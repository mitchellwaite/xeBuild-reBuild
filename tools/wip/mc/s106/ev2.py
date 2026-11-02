import sys
sys.path.insert(0,'../s104'); sys.path.insert(0,'../s86')
import srch, r4sim, m
pre,g,first=r4sim.load('dmp_best/mc.bbro')
def ap(p,gg,w):
    for e,p2,g2 in m.edits(p,gg):
        if e==w: return p2,g2
    raise Exception(w)
for k141 in (None,-10,-8,-6,-5,-4,-3):
  p=list(pre)
  if k141 is not None:
    i=p.index(('visit',141)); p[i]=('push',141,k141)
  p,gg=ap(p,g,('i2p',139,203,-3)); p,gg=ap(p,gg,('mvi',55,49,0,-3))
  o=srch.sim(p,gg); print(k141,srch.dist(o),' '.join(map(str,o)))
