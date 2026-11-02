import sys,itertools,time
import dsim
M=dsim.load(sys.argv[1])
_,o=dsim.sim(M)
print(dsim.score(o))
keys=[0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]
r4blocks=[b for h in M['g4'] for b in [e[1] for e in M['g4'][h] if e[0]=='visit']]
r3blocks=[b for h in M['g3'] for b in [e[1] for e in M['g3'][h] if e[0]=='visit']]
cand=[(b,k,4) for b in r4blocks for k in keys]+[(b,k,3) for b in r3blocks for k in keys]
print(len(cand))
best={}
t=time.time()
for d in cand:
    n,o=dsim.score(dsim.sim(M,{},[d])[1])
    best.setdefault(n,[]).append(d)
print(time.time()-t,{k:len(v) for k,v in sorted(best.items())})
m=max(best)
print(m,best[m][:20])
print(dsim.score(dsim.sim(M,{},[best[m][0]])[1]))
