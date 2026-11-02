# chain3.py DUMP : which r3 entry point/key of a plain dummy D (no ops, or inserting 62) + extras gives 0
import sys
sys.path.insert(0, r'C:/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc/s86'); import r4sim
pre,g,first=r4sim.load(sys.argv[1]); D=9000; DZ=9999
i=first.index(150); TGT=first[:i]+[147,128,150,35,42,53,79,81]+first[i+8:]
def sc(o):
    o=[b for b in o if b<D]; return sum(a!=b for a,b in zip(o,TGT))+abs(len(o)-len(TGT))
ir=max(j for j,e in enumerate(pre) if e[0]=='round')
print([e for e in pre[ir:ir+12]])
base=dict(g); base[69]=[base[69][0],('ins','this',DZ,0)]+base[69][1:]
def tail(o): return [b for b in o if b>=0][17:36]
# with 62 / without 62, and fix for 147/150: 150 inserted in trace 139 before 147
for name,ops in (('D+62',[('visit',D),('ins','this',62,-2)]),('Dplain',[('visit',D)])):
  for fix in (0,1):
    res={}
    for k in (-1,-2,-3,-4,-5,-6):
        for j in range(ir+1,len(pre)+1):
            p=list(pre); p.insert(j,('push',D,k)); gg=dict(base); gg[D]=ops
            if fix:
                L=list(gg[139]); n=[x for x,e in enumerate(L) if e[0]=='ins' and e[2]==147][0]; L.insert(n,('ins','this',150,0)); gg[139]=L
            s=sc(r4sim.sim(p,gg,{})); res.setdefault(s,[]).append((j-len(pre),k))
    b=min(res); print(name,'fix150' if fix else '-',b,len(res[b]),res[b][:16])
