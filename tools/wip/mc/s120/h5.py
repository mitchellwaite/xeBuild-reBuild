exec(open('h1.py').read().split("print('npts'")[0])
import random
random.seed(int(sys.argv[1]))
pts4=[(b,j) for b in g for j in range(len(g[b])+1)]
ptsp=[('p',i) for i in range(len(pre)+1)]
allp=pts4+ptsp
K=[0,0,0,-1,-1,-2,-3,-5,-8,1]
R=list(set(first)|{75,152})
hits=set()
for it in range(150000):
  n=random.randint(1,4); du={}
  for _ in range(n): du[random.choice(allp)]=random.choice(K)
  ov={}
  if random.random()<0.3: ov[random.choice(R)]=random.choice([-1,-2,-3])
  if d(srch.sim(pre,g,ov,du))==0: hits.add((tuple(sorted(du.items(),key=str)),tuple(ov.items())))
print(len(hits))
for h in sorted(hits,key=lambda h:len(h[0])+len(h[1]))[:30]: print(h)
