exec(open('h1.py').read().split("print('npts'")[0])
import time
pts4=[(b,j) for b in g for j in range(len(g[b])+1)]
ptsp=[('p',i) for i in range(len(pre)-60,len(pre)+1)]
P=[(p,k) for p in pts4+ptsp for k in (-1,0)]
R=[(b,k) for b in set(first)|{75,152} for k in (-1,0,-2)]
print(len(P),len(R))
hits=[]
t=time.time()
for x in P:
  if d(srch.sim(pre,g,{},dict([x])))==0: hits.append(('1',x))
for r in R:
  if d(srch.sim(pre,g,dict([r])))==0: hits.append(('r',r))
print('singles',hits,time.time()-t)
for a,c in itertools.combinations(P,2):
  if a[0]==c[0]: continue
  if d(srch.sim(pre,g,{},dict([a,c])))==0: hits.append(('2',a,c))
print('pairs',len(hits),hits[:30],time.time()-t)
for a in P:
  for r in R:
    if d(srch.sim(pre,g,dict([r]),dict([a])))==0: hits.append(('m',a,r))
for a,c in itertools.combinations(R,2):
  if a[0]!=c[0] and d(srch.sim(pre,g,dict([a,c])))==0: hits.append(('rr',a,c))
print('all',len(hits)); 
for h in hits: print(h)
