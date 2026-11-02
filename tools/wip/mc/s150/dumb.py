# dumb.py DUMP [levels] [width] : beam over dummies only (any key 0..-4, any trace/op position) on swapped base; all 0 solutions
import sys, time, multiprocessing as mp
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
D=9999
def init(d):
    global pre,g,first,TGT
    pre,g,first=r4sim.load(d); i=first.index(150); TGT=first[:i]+[147,128,150,35,42,53,79,81]+first[i+8:]
    global CH
    CH=[(G,at,k) for G in first for at in range(1,len(g[G])+1) for k in (0,-1,-2,-3,-4) if g[G][at-1][0]!="chg"]
def sc(o):
    o=[b for b in o if b<D]; return sum(a!=b for a,b in zip(o,TGT))+abs(len(o)-len(TGT))
def run(cs):
    gg=dict(g)
    for n,(G,at,k) in sorted(enumerate(cs),key=lambda x:(-x[1][1],x[0])):
        L=list(gg[G]); L.insert(at,('ins','this',D+1+n,k)); gg[G]=L
    return sc(r4sim.sim(pre,gg,{}))
def work(cs):
    out=[]
    for c in CH:
        if c in cs: continue
        n=tuple(sorted(cs+(c,))); out.append((run(list(n)),n))
    out.sort(key=lambda x:x[0]); 
    return [x for x in out if x[0]==0], out[:800], len(out)
if __name__=='__main__':
    d=sys.argv[1]; LV=int(sys.argv[2]); W=int(sys.argv[3]); init(d); pool=mp.Pool(3,init,(d,)); beam=[()]; sol=set(); t=time.time()
    for lv in range(1,LV+1):
        cand={}; 
        for s0,top,n in pool.imap_unordered(work,beam,2):
            for s,x in s0:
                if x not in sol: sol.add(x); print('SOL',lv,x); sys.stdout.flush()
            for s,x in top: cand[x]=s
        best=sorted(cand.items(),key=lambda x:x[1])[:W]; beam=[x for x,s in best]
        print('level',lv,'best',best[0][1],'worst',best[-1][1],'nsol',len(sol),round(time.time()-t)); sys.stdout.flush()
