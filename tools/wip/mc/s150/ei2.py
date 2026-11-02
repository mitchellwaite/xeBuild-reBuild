# ei2.py DUMP : positions for early insertion of 80 and 82 (usage 3/5 of -r) + optional key-0 dummy by trace 69 on z1
import sys
sys.path.insert(0, r'C:/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc/s86'); import r4sim
pre,g,first=r4sim.load(sys.argv[1]); D=9999
T=[149,129,152,35,42,53,80,82]; i=first.index(149); TGT=first[:i]+T+first[i+8:]
def sc(o):
    o=[b for b in o if b<D]; return sum(a!=b for a,b in zip(o,TGT))+abs(len(o)-len(TGT))
POS=[(G,at) for G in first[:first.index(55)+1] for at in range(1,len(g[G])+1) if g[G][at-1][0]!='chg']
res={}
for dz in (0,1):
  for (G1,a1) in POS:
    for (G2,a2) in POS:
      gg=dict(g)
      if dz: gg[69]=[gg[69][0],('ins','this',D,0)]+gg[69][1:]
      L=list(gg[G1]); L.insert(a1,('ins','this',80,0)); gg[G1]=L
      a=a2+(1 if G2==G1 and a2>a1 else 0)
      L=list(gg[G2]); L.insert(a,('ins','this',82,0)); gg[G2]=L
      s=sc(r4sim.sim(pre,gg,{})); res.setdefault(s,[]).append((dz,G1,a1,G2,a2))
for s in sorted(res)[:3]: print(s,len(res[s]),res[s][:40])
