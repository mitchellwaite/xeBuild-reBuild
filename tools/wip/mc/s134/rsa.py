import sys,random,math
sys.argv=[sys.argv[0],sys.argv[1],'x']+sys.argv[2:]
exec(open('rs.py').read().split("mode=sys.argv[2]")[0].replace("print(","(lambda *a,**k:None)("))
allb=sorted(set(K)|W)
seed=int(sys.argv[3]); pool=T if sys.argv[4]=='T' else allb
random.seed(seed)
bestall=(99,None)
for rs in range(int(sys.argv[5])):
    ov={}; cur=dist(r4sim.sim(pre,g,ov)); temp=2.0
    for it in range(3000):
        n=dict(ov); b=random.choice(pool)
        if b in n and random.random()<0.3: del n[b]
        else: n[b]=random.randint(-8,0)
        try:d=dist(r4sim.sim(pre,g,n))
        except Exception: continue
        c=d+0.05*len(n); cc=cur+0.05*len(ov)
        if c<=cc or random.random()<math.exp((cc-c)/temp): ov,cur=n,d
        temp=max(0.05,temp*0.998)
        if (d,len(n))<(bestall[0],len(bestall[1] or {})+1) and d<=bestall[0]: bestall=(d,dict(n))
    print(rs,cur,len(ov),bestall[0],bestall[1],flush=True)
