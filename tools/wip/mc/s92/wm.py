import r4sim, itertools, sys, copy
pre,g,first=r4sim.load(sys.argv[1])
import tmap,os
_n=os.path.basename(os.path.dirname(sys.argv[1]))
T,_M=tmap.target(_n+'.c','d/%s/order.txt'%_n)
front=first[:first.index(T[1])+1]
pos={b:i for i,b in enumerate(T)}
def score(o):
    if o[:len(front)]!=front: return 999
    q=[pos[b] for b in o if b in pos]
    return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
r3=max(i for i,e in enumerate(pre) if e[0]=='round')
# movable pre events: push/ins next in round 3 tail with low freq
mov=[i for i in range(r3,len(pre)) if (pre[i][0]=='push' and pre[i][2]>-1000000) or (pre[i][0]=='ins' and pre[i][1]=='next')]
print([pre[i] for i in mov])
def premove(p,i,j):
    p=list(p); e=p.pop(i); p.insert(j,e); return p
edits=[]
lo=min(mov)
for i in mov:
    for j in range(lo,len(pre)+1):
        if j in (i,i+1): continue
        edits.append(('pre',i,j))
# round-4 ins moves: move ins of block b from its group to another group (append at end or start)
for src,ev in g.items():
    for k,e in enumerate(ev):
        if e[0]=='ins':
            for dst in first:
                if dst==src: continue
                for where in (0,1,99):
                    edits.append(('g',src,k,dst,where))
def apply(ed,p,gg):
    if ed[0]=='pre':
        return premove(p,ed[1],ed[2]),gg
    _,src,k,dst,where=ed
    gg=dict(gg); s=list(gg[src]); e=s.pop(k); gg[src]=s
    d=list(gg[dst]); d.insert(min(where,len(d)),e); gg[dst]=d; return p,gg
res=[]
for ed in edits:
    p,gg=apply(ed,pre,g)
    try: s=score(r4sim.sim(p,gg,{}))
    except Exception as x: continue
    res.append((s,ed))
res.sort(key=lambda x:x[0])
for r in res[:25]:
    ed=r[1]
    if ed[0]=='pre': print(r[0],'pre move',pre[ed[1]],'-> idx',ed[2],pre[ed[2]] if ed[2]<len(pre) else 'end')
    else: print(r[0],'ins',g[ed[1]][ed[2]],'from',ed[1],'to',ed[3],ed[4])
print('---pairs')
top=[r[1] for r in res if r[0]<=9][:400]
import random
best=[]
for a,b in itertools.combinations(top,2):
    try:
        p,gg=apply(a,pre,g)
        if b[0]=='pre' and a[0]=='pre': continue
        p,gg=apply(b,p,gg)
        o=r4sim.sim(p,gg,{}); s=score(o)
    except Exception: continue
    best.append((s,a,b,o))
best.sort(key=lambda x:x[0])
def desc(ed):
    if ed[0]=='pre': return 'pre %s->%s'%(pre[ed[1]],pre[ed[2]] if ed[2]<len(pre) else 'end')
    return 'ins %s from %s to %s@%s'%(g[ed[1]][ed[2]],ed[1],ed[3],ed[4])
for s,a,b,o in best[:20]: print(s,desc(a),'|',desc(b),'|',' '.join(map(str,o[13:34])))
