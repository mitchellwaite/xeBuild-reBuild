# what-if: move ins events of given blocks to round-3 push list positions / round-4 initial ins
import sys, itertools, r4sim
from r4sim import load
pre,g,first=load(sys.argv[1])
T=[145,49,125,121,107,55,139,138,61,33,29,68,140,127,143,35,42,53,78,80,74]
pos={b:i for i,b in enumerate(T)}
def inv(o):
    q=[pos[b] for b in o if b in pos]; return sum(1 for i in range(len(q)) for j in range(i+1,len(q)) if q[i]>q[j])
i3=max(j for j,e in enumerate(pre) if e==('round',3))
pushidx=[j for j in range(i3,len(pre)) if pre[j][0]=='push']
def run(moves):
    # moves: list of (block, where) where 'pK' = push after K-th push in round 3, 'g:B' = ins in group B end
    p=list(pre); gg={k:list(v) for k,v in g.items()}
    for b,_ in moves:
        for k in gg: gg[k]=[e for e in gg[k] if not (e[0]=='ins' and e[2]==b)]
        p=[e for e in p if not (e[0] in('ins','push') and (e[1]==b or (len(e)>2 and e[2]==b)))]
    ins_after={}
    for b,w in moves:
        if w[0]=='p': ins_after.setdefault(int(w[1:]),[]).append(('push',b,0))
        else: gg.setdefault(int(w[2:]),[]).append(('ins','this',b,0))
    # rebuild p with pushes inserted after K-th push
    out=[];k=0
    i3b=max(j for j,e in enumerate(p) if e==('round',3))
    for j,e in enumerate(p):
        out.append(e)
        if j>i3b and e[0]=='push':
            k+=1; out+=ins_after.get(k,[])
    if 0 in ins_after:
        out=out[:i3b+1]+ins_after[0]+out[i3b+1:]
    return r4sim.sim(out,gg,{})
base=run([]); print(inv(base),[b for b in base if b in pos])
blocks=[int(x) for x in sys.argv[2].split(',')]
opts=['p%d'%k for k in range(0,8)]+['g:%d'%b for b in [145,49,125,121,138,107,55,29,139,61,33,68]]
best=[]
for combo in itertools.product(opts,repeat=len(blocks)):
    o=run(list(zip(blocks,combo))); best.append((inv(o),combo,[b for b in o if b in pos]))
best.sort(key=lambda x:x[0])
for x in best[:8]: print(x)
