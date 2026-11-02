import sys, copy, itertools
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86')
import r4sim
pre, g, first = r4sim.load(sys.argv[1])
base=r4sim.sim(pre,g)
b=[x for x in base if x!=152]
D={}
for a in (35,42,53,79,75,83,88):
    i=b.index(a); D[tuple(b[:i+1]+[152]+b[i+1:])]=a
nodes=sorted(set(base))
hits=0
for n in nodes:
  for k in range(-8,4):
    o=tuple(r4sim.sim(pre,g,{n:k}))
    if o in D: print('HIT1',n,k,D[o]); hits+=1
for n,m in itertools.combinations(nodes,2):
  for k in (-1,0,1,2):
    for l in (-1,0,1,2):
      o=tuple(r4sim.sim(pre,g,{n:k,m:l}))
      if o in D: print('HIT2',n,k,m,l,D[o]); hits+=1
print('hits',hits)
