import sys
exec(open("srchz.py").read())
blocks=sorted(keys); ks=[-1000404,-1000304,-1000204,-1000104,-9,-8,-7,-6,-5,-4,-3,-2,-1,0]
beam=[(dist(base),{},tuple(base))]; seenord={tuple(base)}
for depth in range(5):
    nb=[]
    for d0,ov,po in beam:
        for b in blocks:
            if b in ov: continue
            for k in ks:
                if k==keys.get(b): continue
                o=dict(ov); o[b]=k
                try: r=tuple(r4sim.sim(pre,g,o))
                except Exception: continue
                if r in seenord: continue
                seenord.add(r); nb.append((dist(r),o,r))
    nb.sort(key=lambda x:(x[0],len(x[1]))); beam=nb[:40]
    print(depth,[(d,o) for d,o,_ in beam[:6]],flush=True)
    if beam[0][0]==0: print('ORDER',beam[0][2]); break
