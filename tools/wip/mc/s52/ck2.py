import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s51'))
import es
B=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s47','H5c2.c')).read()
OLD='JUMP(i1, p1, hdd5, hdd4, c10, c9, c1, c7, cdef);'
L='i1, p1, hdd5, hdd4, c10, c9, c1, c7, cdef'
def var(K, lab=L, B=B, old=OLD):
    s=''.join('{ struct {} fkv%d; '%k for k in range(K))
    s+='__asm__ goto ("" :: %s :: %s%s); goto fkN; '%(', '.join('"X"(&fkv%d)'%k for k in range(K)), lab, ''.join(', fk%d'%k for k in range(K)))
    s+=''.join('fk%d: ; } '%k for k in reversed(range(K)))
    s+='fkN: ;'
    return B.replace(old,s)
if __name__=='__main__':
    for K in map(int,sys.argv[1:]):
        r=es.run(var(K),'s52d%d'%K,fncmp=False); print(K,r,flush=True)
