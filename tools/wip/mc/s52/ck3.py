"""two asm gotos with fake labels whose clobber-copy blocks vanish at RTL and merge into the fallthrough."""
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s51'))
import es
B=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s47','H5c2.c')).read()
OLD='JUMP(i1, p1, hdd5, hdd4, c10, c9, c1, c7, cdef);'
L=['i1','p1','hdd5','hdd4','c10','c9','c1','c7','cdef']
def var(split=5, k1=None, k2=None, B=B, old=OLD, labs=L, useasm=True):
    r1, r2 = labs[:split], labs[split:]
    k1 = 30-len(r1) if k1 is None else k1; k2 = 30-len(r2) if k2 is None else k2
    fa=['fa%d'%k for k in range(k1)]; fb=['fb%d'%k for k in range(k2)]
    s='{ struct {} fko; { struct {} fkv; '
    if useasm: s+='__asm__ ("" :: "X"(&fko), "X"(&fkv)); '
    s+='__asm__ goto ("" :::: %s); fkA2: '%', '.join(r1+fa)
    if r2: s+='__asm__ goto ("" :::: %s); '%', '.join(r2+fb)
    s+='goto fkN; '
    s+=' '.join('%s: goto o%s;'%(x,x) for x in fa)+' '
    s+=' '.join('%s: goto o%s;'%(x,x) for x in fb)+' '
    s+='} '+' '.join('o%s: goto fkA2;'%x for x in fa)+' '+' '.join('o%s: goto fkM;'%x for x in fb)+' fkM: ; } fkN: ;'
    return B.replace(old,s)
if __name__=='__main__':
    for a in sys.argv[1:]:
        sp,k1,k2=[int(x) for x in a.split(',')]
        r=es.run(var(sp,k1,k2),'s52e%s'%a.replace(',','_'),fncmp=False); print(a,r,flush=True)
