import sys,os,json
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s51'))
import es
B=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s47','H5c2.c')).read()
OLD='JUMP(i1, p1, hdd5, hdd4, c10, c9, c1, c7, cdef);'
def var(lbl): return B.replace(OLD, 'JMP(%s);'%lbl if lbl else '')
if __name__=='__main__':
    for i,l in enumerate(sys.argv[1:]):
        r=es.run(var(l),'s52v%d'%i,fncmp=False); print(l,r,flush=True)
