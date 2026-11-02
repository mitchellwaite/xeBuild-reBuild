"""s1.py: chained rok asm (cap) with exact target weights; prints es2 per variant."""
import sys,os,json
D=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(D,'..','s54')); sys.path.insert(0,os.path.join(D,'..','s53'))
import rkgen,lev,es2
V={
 'base':({'p0':1,'c3':2},30),
 'cap14':({'p0':1,'c3':2},14),
 'ex30':({'cdef':6,'hdd4':3,'hdd5':3,'u2':2},30),
 'ex16':({'cdef':6,'hdd4':3,'hdd5':3,'u2':2},16),
 'ex8':({'cdef':6,'hdd4':3,'hdd5':3,'u2':2},8),
 'exc3':({'cdef':6,'hdd4':3,'hdd5':3,'u2':2,'c3':2,'p0':1},16),
}
sel=sys.argv[1:] or list(V)
for k in sel:
    w,cap=V[k]; s=lev.text({}); s=s.replace(rkgen.rok({'p0':1,'c3':2}),'@@',1) if False else s
    t=lev.B0
    # rebuild via lev with custom cap
    old=rkgen.mk; rkgen.mk=lambda ww,base=None,_c=cap: old(ww,cap=_c,base=base)
    try: txt=lev.text({'w':w})
    finally: rkgen.mk=old
    r=es2.run(txt,'s55'+k,False)
    print(k,cap,r and (r.get('es2'),r.get('per2'),r.get('ev')),flush=True)
