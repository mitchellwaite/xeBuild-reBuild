"""sim3: rounds 3+4 dynamic replay: r3 traces popped from the model heap (groups per head), so r3 tie changes propagate to r4."""
import sys,os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import fibsim
def load(dump):
    ev=fibsim.parse(dump)
    i3=ev.index(('round',3)); i4=ev.index(('round',4))
    pre=ev[:i3]
    def grp(l):
        gs={};cur=None;first=[]
        for e in l:
            if e[0]=='get':
                cur=e[1]; first.append(cur); gs.setdefault(cur,[]); continue
            gs[cur].append(e)
        return gs,first
    g3,f3=grp(ev[i3+1:i4]); g4,f4=grp(ev[i4+1:])
    return pre,g3,f3,g4,f4
def sim(pre,g3,g4,ov={},r3trace=None):
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
    # round 3
    heap=new; new=fibsim.Heap()
    loc={b:v for b,v in loc.items() if v[0] is heap}
    vis=set(); o3=[]
    def step(b,gs,this,nxt):
        for e in gs.get(b,[]):
            if e[0]=='visit':
                vis.add(e[1])
                if e[1] in loc: h,n=loc.pop(e[1]); h.delete_node(n)
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
                    hh,n=loc[e[1]]; 
                    if hh is not nxt: hh.delete_node(n)
                    else:
                        continue
                loc[e[1]]=(nxt,nxt.insert(ov.get(e[1],e[2]),e[1]))
            elif e[0]=='chg':
                if e[1] in loc:
                    h,n=loc[e[1]]; loc[e[1]]=(h,h.replace_key(n,ov.get(e[1],e[2])))
    while heap.min is not None:
        z=heap.extract_min(); b=z.data; loc.pop(b,None)
        if b in vis: continue
        o3.append(b)
        step(b,g3,heap,new)
    heap=new; loc={b:v for b,v in loc.items() if v[0] is heap}
    o4=[]
    dummy=fibsim.Heap()
    while heap.min is not None:
        z=heap.extract_min(); b=z.data; loc.pop(b,None)
        if b in vis: continue
        o4.append(b)
        step(b,g4,heap,dummy)
    return o3,o4
if __name__=='__main__':
    pre,g3,f3,g4,f4=load(sys.argv[1])
    o3,o4=sim(pre,g3,g4)
    print('r3 same',o3==f3,len(o3),len(f3)); print('r4 same',o4==f4,len(o4),len(f4))
    if o3!=f3: print(f3[:20]);print(o3[:20])
