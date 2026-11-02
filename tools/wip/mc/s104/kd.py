import sys,itertools;sys.path.insert(0,'s104');from srch import *
pre,g,f=r4sim.load(sys.argv[1])
r3 = pre.index(('round', 3)); pts = [('p', i + 1) for i in range(r3, len(pre)) if pre[i][0] == 'visit'] + [(b, j) for b in g for j in range(len(g[b]) + 1)]
B=(139,29,33,55)
best=[]
for ks in itertools.product((-3,-2,-1),repeat=4):
  ov=dict(zip(B,ks))
  d0=dist(sim(pre,g,ov)); best.append((d0,ks,None))
  for p in pts:
    for k in (-3,-2,-1,0):
      d=dist(sim(pre,g,ov,{p:k}))
      if d<=1: best.append((d,ks,p,k))
best.sort(key=lambda r:r[0]); print(best[:30])
