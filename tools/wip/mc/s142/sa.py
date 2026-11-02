import sys,random,math
exec(open('srch.py').read().split("print('d0'")[0])
blocks=list(keys); ks=[-1000404,-1000304,-1000204,-1000104,-9,-8,-7,-6,-5,-4,-3,-2,-1,0]
random.seed(int(sys.argv[2])); best=None
for run in range(4):
    ov={};cur=dist(r4sim.sim(pre,g));Tm=2.0
    for it in range(5000):
        o=dict(ov); r=random.random()
        if r<0.6 or not o: o[random.choice(blocks)]=random.choice(ks)
        elif r<0.85: o.pop(random.choice(list(o)))
        else: b=random.choice(list(o)); o[b]=random.choice(ks)
        try: d=dist(r4sim.sim(pre,g,o))
        except Exception: continue
        c=d+0.3*len(o); cc=cur+0.3*len(ov)
        if c<=cc or random.random()<math.exp((cc-c)/Tm): ov,cur=o,d
        Tm=max(0.05,Tm*0.999)
        if best is None or (d,len(ov))<best[:2]: best=(d,len(ov),dict(ov))
    print(run,best,flush=True)
