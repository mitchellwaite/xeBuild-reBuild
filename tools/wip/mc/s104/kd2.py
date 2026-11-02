import sys,itertools,time;sys.path.insert(0,'s104');from srch import *
pre,g,f=r4sim.load(sys.argv[1])
r3 = pre.index(('round', 3)); pts = [('p', i + 1) for i in range(r3, len(pre)) if pre[i][0] == 'visit'] + [(b, j) for b in f[:22] for j in range(len(g[b]) + 1)]
print(len(pts))
res=[]
for ks in itertools.product((-3,-2),(-1,-2),(-2,-1),(-3,-2)):
  ov=dict(zip((139,29,33,55),ks)); ov[139]=max(ov[139],-2) if 0 else ov[139]
  for a,b in itertools.combinations(pts,2):
    for ka in (-3,-2,-1):
      for kb in (-3,-2,-1):
        d=dist(sim(pre,g,ov,{a:ka,b:kb}))
        if d==0: print('ZERO',ks,a,ka,b,kb); sys.stdout.flush()
print('done')
