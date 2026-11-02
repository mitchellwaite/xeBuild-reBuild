# chain.py DUMP : zero-byte forwarder D (asm goto k61l + unreachable) popped in r4, inserting 62 (-w test) early with no back edge.
# D enters the r4 heap from the end of round 3 (offset) or from a trace position, with key k; + optional key-0 dummy by trace 69.
import sys
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
pre,g,first=r4sim.load(sys.argv[1]); D=9000; DZ=9999
i=first.index(150); TGT=first[:i]+[147,128,150,35,42,53,79,81]+first[i+8:]
def sc(o):
    o=[b for b in o if b<D]; return sum(a!=b for a,b in zip(o,TGT))+abs(len(o)-len(TGT))
print([ (e[2],e[3]) if e[0]=='ins' else e for e in pre[-30:]][:30])
res={}
K=(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12)
for dz in (0,1):
  for keep in (1,0):
    def base():
        gg=dict(g); gg[D]=[('visit',D),('ins','this',62,-2)]
        if dz: gg[69]=[gg[69][0],('ins','this',DZ,0)]+gg[69][1:]
        if not keep: gg[55]=[e for e in gg[55] if not(e[0]=='ins' and e[2]==62)]
        return gg
    for k in K:
        for off in range(0,12):
            p=list(pre); p.insert(len(p)-off,('push',D,k))
            s=sc(r4sim.sim(p,base(),{})); res.setdefault(s,[]).append(('pre',off,k,dz,keep))
        for G in first[:20]:
            for at in range(1,len(g[G])+1):
                gg=base(); L=list(gg[G]); L.insert(at,('ins','this',D,k)); gg[G]=L
                s=sc(r4sim.sim(pre,gg,{})); res.setdefault(s,[]).append((G,at,k,dz,keep))
for s in sorted(res)[:4]: print(s,len(res[s]),res[s][:14])
# full round-3 scan: D pushed at any r3 op index
ir=max(j for j,e in enumerate(pre) if e[0]=='round'); print('r3 ops',len(pre)-ir)
res={}
for dz in (0,1):
    gg=dict(g); gg[D]=[('visit',D),('ins','this',62,-2)]
    if dz: gg[69]=[gg[69][0],('ins','this',DZ,0)]+gg[69][1:]
    for k in K:
        for j in range(ir+1,len(pre)+1):
            p=list(pre); p.insert(j,('push',D,k))
            try: s=sc(r4sim.sim(p,gg,{}))
            except Exception: continue
            res.setdefault(s,[]).append((j-len(pre),k,dz))
for s in sorted(res)[:3]: print(s,len(res[s]),res[s][:24])
