import sys, copy
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86')
import r4sim
pre, g, first = r4sim.load(sys.argv[1])
base=r4sim.sim(pre,g)
b=[x for x in base if x!=152]
D={}
for a in (35,42,53,79,75,83):
    i=b.index(a); D[a]=b[:i+1]+[152]+b[i+1:]
best=[]
for grp in first:
  for p in range(len(g.get(grp,[]))+1):
    for k in (-2,-1,0,1):
      G=copy.deepcopy(g); G[149]=[e for e in G[149] if not(e[0]=='ins' and e[2]==152)]
      G.setdefault(grp,[]); G[grp]=G[grp][:p]+[('ins','this',152,k)]+G[grp][p:]
      o=r4sim.sim(pre,G)
      for a,d in D.items():
        if o==d: print('HIT',a,grp,p,k)
      # count mismatches excluding 152
      oo=[x for x in o if x!=152]
      if oo==b: best.append((grp,p,k,o.index(152) if 152 in o else -1))
print('preserving-others:',best)
