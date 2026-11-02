# m.py: broadened round-3/4 model. state = (pre, groups) edited event lists, simulated by srch.sim
import sys, itertools, copy
sys.path.insert(0,'../s104'); sys.path.insert(0,'../s86')
import srch, r4sim
T=srch.T
def D(pre,g): return srch.dist(srch.sim(pre,g))
def tail_idx(pre):
    i=max(j for j,e in enumerate(pre) if e==('round',3)); return i
def edits(pre,g):
    """yield (desc, pre2, g2)"""
    i3=tail_idx(pre)
    # (a1) swap adjacent get/push pairs in round 3 tail
    pairs=[j for j in range(i3,len(pre)-1) if pre[j][0]=='get' and pre[j+1][0]=='push']
    for a,b in zip(pairs,pairs[1:]):
        if b==a+2:
            p=list(pre); p[a:a+4]=pre[b:b+2]+pre[a:a+2]; yield ('swp',pre[a][1],pre[b][1]),p,g
    # (a2) move a round-3 push to the end / start of tail
    for a in pairs:
        p=list(pre); seg=p[a:a+2]; del p[a:a+2]
        for t in [x for x in range(i3+1,len(p)+1) if x==len(p) or p[x][0]=='get']:
            if t==a: continue
            q=p[:t]+seg+p[t:]; yield ('mvp',pre[a][1],t),q,g
    # (a3) a round-4 'ins' block instead pushed in round 3 at position t with key k
    for b0,ev in g.items():
        for j,e in enumerate(ev):
            if e[0]!='ins': continue
            g2=dict(g); g2[b0]=ev[:j]+ev[j+1:]
            for t in [x for x in range(i3+1,len(pre)+1) if x==len(pre) or pre[x][0]=='get']:
                for k in (-4,-3,-2,-1,0):
                    yield ('i2p',e[2],t,k),pre[:t]+[('get',e[2]),('push',e[2],k)]+pre[t:],g2
    # (b) move/rekey a round-4 insertion to another group position
    allpos=[(b,j) for b in g for j in range(len(g[b])+1)]
    for b0,ev in g.items():
        for j,e in enumerate(ev):
            if e[0]!='ins': continue
            for (b1,j1) in allpos:
                for k in (-4,-3,-2,-1,0):
                    if (b1,j1) in ((b0,j),(b0,j+1)) and k==e[3]: continue
                    g2=dict(g); g2[b0]=ev[:j]+ev[j+1:]
                    l=list(g2[b1]); jj=j1-(1 if b1==b0 and j1>j else 0); l.insert(jj,('ins','this',e[2],k)); g2[b1]=l
                    yield ('mvi',e[2],b1,jj,k),pre,g2
    # (c) dummy insert anywhere in round 4 groups / round 3 tail pushes
    for (b1,j1) in allpos:
        for k in (-4,-3,-2,-1,0):
            g2=dict(g); l=list(g2[b1]); l.insert(j1,('ins','this',9000+len(l)*0+hash((b1,j1,k))%900+9001,k)); g2[b1]=l
            yield ('dum',b1,j1,k),pre,g2
if __name__=='__main__':
    pre,g,first=r4sim.load(sys.argv[1]); W=int(sys.argv[2]) if len(sys.argv)>2 else 60; depth=int(sys.argv[3]) if len(sys.argv)>3 else 3
    beam=[(D(pre,g),(),pre,g)]; print('base',beam[0][0]); seen=set()
    for d in range(depth):
        nb=[]
        for s,desc,p,gg in beam:
            for e,p2,g2 in edits(p,gg):
                o=srch.sim(p2,g2); key=tuple(o)
                if key in seen: continue
                seen.add(key); nb.append((srch.dist(o),desc+(e,),p2,g2))
        nb.sort(key=lambda r:(r[0],len(r[1])))
        beam=nb[:W]
        print('depth',d+1,'best',beam[0][0]); 
        for r in beam[:12]: print(' ',r[0],r[1])
        if beam[0][0]==0: break
