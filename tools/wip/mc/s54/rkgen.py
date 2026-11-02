"""gen.py: rok dispatch with per-target fake weights. mk(w, order=None, cap=30) -> C text.
w: dict label->extra fake count. Fakes: clobber-only copies (s52 construct) that cfgcleanup forwards into the target."""
import os,sys
D=os.path.dirname(os.path.abspath(__file__))
B=open(os.path.join(D,'base.c')).read()
RL=['c12','c11','p0','i0','c9','hdd4','hdd5','c2','c1','c10','u2','cdef','c8','c7','c3','s5']
OLD='JUMP(c12, c11, p0, i0, c9, hdd4, hdd5, c2, c1, c10, u2, cdef, c8, c7, c3, s5);'
def rok(w,order=None,cap=30,real=True,pref='rk'):
    labs=list(order or RL) if real else []
    fk=[]
    for l in list(order or RL)+['_ft']:
        for j in range(w.get(l,0)): fk.append(l if l!='_ft' else pref+'E')
    allt=[(x,None) for x in labs]+[('%s%d'%(pref,i),t) for i,t in enumerate(fk)]
    chunks=[allt[i:i+cap] for i in range(0,len(allt),cap)] or [[]]
    s='{ struct {} %so; '%pref; inner=''; outer=''
    for ci,ch in enumerate(chunks):
        s+='{ struct {} %sv%d; __asm__ ("" :: "X"(&%so), "X"(&%sv%d)); __asm__ goto ("" :::: %s); goto %sn%d; '%(pref,ci,pref,pref,ci,', '.join(x for x,_ in ch),pref,ci)
        for x,t in ch:
            if t: s+='%s: goto o%s; '%(x,x); outer+='o%s: goto %s; '%(x,t)
        s+='} %sn%d: ; '%(pref,ci)
    s+='goto %sE; '%pref+outer+'} %sE: ; '%pref
    # outer gotos placed inside the outer scope but after inner scopes
    return s
def mk(w,order=None,cap=30,real=True,base=None):
    b=base or B; assert OLD in b
    return b.replace(OLD,rok(w,order,cap,real),1)
if __name__=='__main__':
    print(rok({'c12':2,'c1':1}))
import re as _re
FL=['i1','p1','hdd5','hdd4','c10','c9','c1','c7','cdef']
FOLD=_re.search(r'fkbo: \{ struct \{\} fko;.*?fkN: ;',B).group(0)
def fk(groups,pref='fq'):
    """groups: list of (reals, nfakes) chained asm gotos; fakes forward to the chain's end (pref+'E')."""
    s='fkbo: { struct {} %so; '%pref; outer=''; n=0
    for ci,(reals,k) in enumerate(groups):
        labs=list(reals)+['%s%d'%(pref,n+j) for j in range(k)]
        s+='{ struct {} %sv%d; __asm__ ("" :: "X"(&%so), "X"(&%sv%d)); __asm__ goto ("" :::: %s); goto %sn%d; '%(pref,ci,pref,pref,ci,', '.join(labs),pref,ci)
        for j in range(k): s+='%s%d: goto o%s%d; '%(pref,n+j,pref,n+j); outer+='o%s%d: goto %sE; '%(pref,n+j,pref)
        n+=k; s+='} %sn%d: ; '%(pref,ci)
    return s+'goto %sE; '%pref+outer+'} %sE: ;'%pref
def mk2(w,groups=None,order=None,cap=30,real=True,base=None):
    b=base or B
    if groups is not None: b=b.replace(FOLD,fk(groups),1)
    return mk(w,order,cap,real,base=b) if w is not None else b
