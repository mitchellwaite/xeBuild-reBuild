import sys, copy
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86')
import r4sim
pre, g, first = r4sim.load(sys.argv[1])
want=r4sim.sim(pre,g,{152:1,75:1})
# where is 75 inserted?
for grp,ev in g.items():
  for e in ev:
    if e[0] in('ins','chg') and (e[1]==75 or (len(e)>2 and e[2]==75)): print('75 in',grp,e)
for e in pre:
  if (e[0]=='ins' and e[2]==75) or (e[0]=='push' and e[1]==75) or (e[0]=='chg' and e[1]==75): print('pre',e)
print(g[69])
hits=[]
for grp in first:
  for p in range(len(g.get(grp,[]))+1):
    G=copy.deepcopy(g); G[149]=[e for e in G[149] if not(e[0]=='ins' and e[2]==152)]
    G[grp]=G[grp][:p]+[('ins','this',152,0)]+G[grp][p:]
    o=r4sim.sim(pre,G)
    if o==want: hits.append((grp,p))
print('152 moved hits',hits)
# also: remove 75 ins and move it too
hits=[]
for g1 in first:
 for g2 in first:
    G=copy.deepcopy(g); G[149]=[e for e in G[149] if not(e[0]=='ins' and e[2]==152)]
    G[69]=[e for e in G[69] if not(e[0]=='ins' and e[2]==75)]
    G[g1]=G[g1]+[('ins','this',152,0)]; G[g2]=G[g2]+[('ins','this',75,0)]
    if r4sim.sim(pre,G)==want: hits.append((g1,g2))
print('both',hits)
