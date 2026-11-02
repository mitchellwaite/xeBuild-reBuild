# m2.py: realizable-restricted beam. edits: rekey any round-4 ins in place; mvi only within same group;
# rekey round-3 pushes; swap adjacent round-3 pushes; dummies (round-4 groups); no i2p for clientEraseBlockI blocks
import sys
sys.path.insert(0,'../s104'); sys.path.insert(0,'../s86')
import srch, r4sim, m
EB={134,135,136,137,138,139,140}
def edits(pre,g):
    i3=m.tail_idx(pre)
    for e,p2,g2 in m.edits(pre,g):
        if e[0]=='i2p' and e[1] in EB: continue
        if e[0]=='mvi':
            # find source group
            src=[b for b in g if any(x[0]=='ins' and x[2]==e[1] for x in g[b])]
            if src and src[0]!=e[2]: continue
        yield e,p2,g2
    for j in range(i3,len(pre)):
        if pre[j][0]=='push':
            for k in (-4,-3,-2,-1,0) if pre[j][2]>-1000 else (pre[j][2]-2,pre[j][2]-1,pre[j][2]+1,pre[j][2]+2):
                if k==pre[j][2]: continue
                p=list(pre); p[j]=('push',pre[j][1],k); yield ('rkp',pre[j][1],k),p,g
if __name__=='__main__':
    pre,g,first=r4sim.load(sys.argv[1])
    if len(sys.argv)>4 and sys.argv[4]!='-':
        i=pre.index(('visit',141)); pre[i]=('push',141,int(sys.argv[4]))
    W=int(sys.argv[2]); depth=int(sys.argv[3])
    beam=[(srch.dist(srch.sim(pre,g)),(),pre,g)]; print('base',beam[0][0],' '.join(map(str,srch.sim(pre,g)))); seen=set()
    for d in range(depth):
        nb=[]
        for s,desc,p,gg in beam:
            for e,p2,g2 in edits(p,gg):
                o=srch.sim(p2,g2); key=tuple(o)
                if key in seen: continue
                seen.add(key); nb.append((srch.dist(o),desc+(e,),p2,g2,o))
        nb.sort(key=lambda r:(r[0],len(r[1])))
        beam=[r[:4] for r in nb[:W]]
        print('depth',d+1,'best',nb[0][0],' '.join(map(str,nb[0][4])),flush=True)
        for r in nb[:10]: print(' ',r[0],r[1])
        if nb[0][0]==0: break
