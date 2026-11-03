"""dsim.py: exact bbro heap model for mode_update's rounds 3-4 from a bbro dump, with what-ifs.
sim(M, ov={bb:key}, dum=[(bb, key, round)]) -> r4 extraction order without dummies.
dum: when block bb is visited in that round, dummy node with key is inserted (r4: this heap; r3: next-round heap).
WANT/FLEX as tools/wip/fibsolve.py. python dsim.py DUMP checks the model against the dump."""
import sys,os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import fibsim
WANT=[43,128,81,87,82,130,73,69,77,102,112,46,90,122,118,94,48,117,20,125,50,30,38,54,58,64,62]
FLEX={44,105,13}
def load(dump):
    t=open(dump).read()
    if t.count(';; Function')>1: t=t[t.index(';; Function mode_update'):]
    open(dump+'.mu','w').write(t)
    ev=fibsim.parse(dump+'.mu')
    i3=ev.index(('round',3)); i4=ev.index(('round',4))
    def grp(l):
        gs={};cur=None;first=[]
        for e in l:
            if e[0]=='get':
                cur=e[1]; first.append(cur); gs.setdefault(cur,[]); continue
            gs[cur].append(e)
        return gs,first
    g3,f3=grp(ev[i3+1:i4]); g4,f4=grp(ev[i4+1:])
    return dict(pre=ev[:i3],g3=g3,f3=f3,g4=g4,f4=f4)
def sim(M,ov={},dum=()):
    pre,g3,g4=M['pre'],M['g3'],M['g4']
    heap=fibsim.Heap(); loc={2:(heap,heap.insert(0,2))}; new=None
    for e in pre:
        if e[0]=='round':
            if new is not None: heap=new
            new=fibsim.Heap()
        elif e[0]=='get':
            heap.extract_min(); loc.pop(e[1],None)
        elif e[0]=='visit':
            if e[1] in loc: h,n=loc.pop(e[1]); h.delete_node(n)
        elif e[0]=='ins':
            h=heap if e[1]=='this' else new
            loc[e[2]]=(h,h.insert(ov.get(e[2],e[3]),e[2]))
        elif e[0]=='push':
            loc[e[1]]=(new,new.insert(ov.get(e[1],e[2]),e[1]))
        elif e[0]=='chg':
            h,n=loc[e[1]]; loc[e[1]]=(h,h.replace_key(n,ov.get(e[1],e[2])))
    heap=new; new=fibsim.Heap()
    loc={b:v for b,v in loc.items() if v[0] is heap}
    vis=set(); dv={}
    for b,k,r in dum: dv.setdefault((b,r),[]).append(k)
    did=0
    def step(b,gs,this,nxt,rn):
        nonlocal did
        for e in gs.get(b,[]):
            if e[0]=='visit':
                vis.add(e[1])
                if e[1] in loc: h,n=loc.pop(e[1]); h.delete_node(n)
                for k in dv.get((e[1],rn),()):
                    did+=1
                    (this if rn==4 else nxt).insert(k,('d',did))
            elif e[0]=='ins':
                h=this if e[1]=='this' else nxt
                if e[2] in vis: continue
                if e[2] in loc:
                    k=ov.get(e[2],e[3]); hh,n=loc[e[2]]
                    if n.key!=k: loc[e[2]]=(hh,hh.replace_key(n,k))
                    continue
                loc[e[2]]=(h,h.insert(ov.get(e[2],e[3]),e[2]))
            elif e[0]=='push':
                if e[1] in vis: continue
                if e[1] in loc:
                    hh,n=loc[e[1]]
                    if hh is not nxt: hh.delete_node(n)
                    else: continue
                loc[e[1]]=(nxt,nxt.insert(ov.get(e[1],e[2]),e[1]))
            elif e[0]=='chg':
                if e[1] in loc:
                    h,n=loc[e[1]]; loc[e[1]]=(h,h.replace_key(n,ov.get(e[1],e[2])))
    o3=[]
    while heap.min is not None:
        z=heap.extract_min(); b=z.data; loc.pop(b,None)
        if isinstance(b,tuple): continue
        if b in vis: continue
        o3.append(b)
        step(b,g3,heap,new,3)
    heap=new; loc={b:v for b,v in loc.items() if v[0] is heap}
    o4=[]; dummy=fibsim.Heap()
    while heap.min is not None:
        z=heap.extract_min(); b=z.data; loc.pop(b,None)
        if isinstance(b,tuple): continue
        if b in vis: continue
        o4.append(b)
        step(b,g4,heap,dummy,4)
    return o3,o4
def score(o4):
    o=[b for b in o4 if b not in FLEX]
    # longest common prefix, number of positions off
    n=0
    for a,b in zip(o,WANT):
        if a!=b: break
        n+=1
    return n,o
if __name__=='__main__':
    M=load(sys.argv[1])
    o3,o4=sim(M)
    print('r3 same',o3==M['f3'],'r4 same',o4==M['f4'])
    print(score(o4))
