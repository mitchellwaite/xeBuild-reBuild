# chain2.py DUMP : D (key k) pushed at end of round 3, inserting 62 on pop + dum69; then 1-2 extra dummies/keyed
import sys
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
pre,g,first=r4sim.load(sys.argv[1]); D=9000; DZ=9999
i=first.index(150); TGT=first[:i]+[147,128,150,35,42,53,79,81]+first[i+8:]
def sc(o):
    o=[b for b in o if b<D]; return sum(a!=b for a,b in zip(o,TGT))+abs(len(o)-len(TGT))
for off,k in ((1,-3),(1,-4),(58,-3),(58,-4)):
    p=list(pre); p.insert(len(p)-off,('push',D,k))
    gb=dict(g); gb[D]=[('visit',D),('ins','this',62,-2)]; gb[69]=[gb[69][0],('ins','this',DZ,0)]+gb[69][1:]
    o=r4sim.sim(p,gb,{}); print(off,k,sc(o),o[:36])
    CH=[(G,at,kk) for G in first+[D] for at in range(1,len(gb[G])+1) for kk in (0,-1,-2,-3) if gb[G][at-1][0]!='chg']
    def run(cs):
        gg=dict(gb)
        for n,(G,at,kk) in sorted(enumerate(cs),key=lambda x:-x[1][1]):
            L=list(gg[G]); L.insert(at,('ins','this',DZ+1+n,kk)); gg[G]=L
        return sc(r4sim.sim(p,gg,{}))
    S=sorted((run([c]),c) for c in CH); print(S[:6])
    top=[c for s,c in S if s<=5][:120]; n=0
    for a in top:
        for b in CH:
            if run([a,b])==0:
                n+=1
                if n<12: print(' SOL2',a,b)
    print(' nsol2',n)
