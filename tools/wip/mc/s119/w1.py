import sys, copy
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86')
import r4sim
pre, g, first = r4sim.load(sys.argv[1])
e152=[e for e in g[149] if e[0]=='ins' and e[2]==152]
print('ev',e152, [e for e in g[149]])
print('base',' '.join(map(str,r4sim.sim(pre,g))))
for grp in first:
  for pos in ('start','end'):
    G=copy.deepcopy(g); G[149]=[e for e in G[149] if not(e[0]=='ins' and e[2]==152)]
    if pos=='start': G[grp]=e152+G[grp]
    else: G[grp]=G[grp]+e152
    o=r4sim.sim(pre,G)
    s=' '.join(map(str,o)); i=o.index(152) if 152 in o else -1
    print(grp,pos,s[s.find('131'):])
