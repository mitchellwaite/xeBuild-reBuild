import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s51'))
import es
B=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s47','H5c2.c')).read()
OLD='JUMP(i1, p1, hdd5, hdd4, c10, c9, c1, c7, cdef);'
L='i1, p1, hdd5, hdd4, c10, c9, c1, c7, cdef'
def var(K, lab=L, inp='"X"(&fka), "X"(&fkb)'):
    fl=''.join(', fk%d'%k for k in range(K))
    s=('{ struct {} fka; { struct {} fkb; __asm__ goto ("" :: %s :: %s%s); goto fkN; }'%(inp,lab,fl)
       + ''.join(' fk%d:'%k for k in range(K)) + ' ; } fkN: ;')
    return B.replace(OLD,s)
if __name__=='__main__':
    for K in map(int,sys.argv[1:]):
        r=es.run(var(K),'s52c%d'%K,fncmp=False); print(K,r,flush=True)
