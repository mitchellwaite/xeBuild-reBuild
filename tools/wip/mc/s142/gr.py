import sys
exec(open('srch.py').read().split("print('d0'")[0])
blocks=sorted(keys); ks=[-1000404,-1000304,-1000204,-1000104,-9,-8,-7,-6,-5,-4,-3,-2,-1,0]
base=eval(sys.argv[2]) if len(sys.argv)>2 else {}
print('start',dist(r4sim.sim(pre,g,base)))
res=[]
for b in blocks:
    for k in ks:
        o=dict(base); o[b]=k
        try: d=dist(r4sim.sim(pre,g,o))
        except Exception: continue
        res.append((d,b,k))
res.sort(); print(res[:25])
