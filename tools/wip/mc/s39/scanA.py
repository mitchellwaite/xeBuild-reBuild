import sys, json, itertools
from multiprocessing import Pool
sys.path.insert(0,'.')
import m, loopsites as L, cm
T=open(sys.argv[3] if len(sys.argv)>3 else 'best_g7b_dup.c').read()
LABS='c1 c2 c3 s4 hdd4 s5 hdd5 c7 p0 p1 c8 c9 c10 c11 c12 i0 i1 cdef u2'.split()
def job(a):
    tag, edits = a
    t=T
    try:
        for s,tg in edits: t=L.add(t,s,tg)
    except Exception as e: return tag,edits,{'err':repr(e)}
    r=m.meas(t,tag,True)
    if 'err' not in r:
        r['cm']=cm.cm(m.os.path.join(m.D,'v_%s.c'%tag))
    r.pop('fq',None); r.pop('raw',None)
    return tag,edits,r
if __name__=='__main__':
    jobs=json.load(open(sys.argv[1])); out=open(sys.argv[2],'a')
    with Pool(4) as p:
        for tag,ed,r in p.imap_unordered(job,jobs):
            out.write(json.dumps([tag,ed,r])+'\n'); out.flush()
