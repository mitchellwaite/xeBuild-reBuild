# dumk.py DUMP : on swapped base + key-0 dummy by trace 69, enumerate 1-2 further dummies of any key/position
import sys, time
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
pre,g,first=r4sim.load(sys.argv[1]); D=9999
i=first.index(150); TGT=first[:i]+[147,128,150,35,42,53,79,81]+first[i+8:]
def sc(o):
    o=[b for b in o if b<D]; return sum(a!=b for a,b in zip(o,TGT))+abs(len(o)-len(TGT))
g=dict(g); g[69]=[g[69][0],('ins','this',D,0)]+g[69][1:]
print('base+dum69',sc(r4sim.sim(pre,g,{})))
CH=[(G,at,k) for G in first for at in range(len(g[G])+1) for k in (0,-1,-2,-3,-4,-5,-6)]
# dedupe positions: only positions right after a visit or an ins matter; keep all
def run(cs):
    gg=dict(g)
    for n,(G,at,k) in sorted(enumerate(cs),key=lambda x:-x[1][1]):
        L=list(gg[G]); L.insert(at,('ins','this',D+1+n,k)); gg[G]=L
    return sc(r4sim.sim(pre,gg,{}))
S=[(run([c]),c) for c in CH]; S.sort(key=lambda x:x[0]); print(len(CH),S[:12])
top=[c for s,c in S if s<=7][:400]; print('top',len(top))
best={}
for a in top:
    for b in CH:
        s=run([a,b]); 
        if s<=1: print('P',s,a,b); sys.stdout.flush()
        best[s]=best.get(s,0)+1
print(sorted(best.items())[:6])
