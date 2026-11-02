"""scanT.py JOBS OUT: jobs = [tag, [[old,new],...]] textual replacements on g7b."""
import sys, json, os
from multiprocessing import Pool
sys.path.insert(0,'.')
import m, ev
T=open('best_g7b_dup.c').read()
def job(a):
    tag, reps = a; t=T
    for o,n in reps:
        if o not in t: return tag,reps,{'err':'norep '+o}
        t=t.replace(o,n,1)
    r=m.meas(t,tag,True)
    if 'order' in r:
        inv,miss,o=ev.score_order(r['order'].split()[1:]); r['tinv']=inv+5*len(miss); r['o']=' '.join(map(str,o))
    r.pop('fq',None); r.pop('raw',None)
    return tag,reps,r
if __name__=='__main__':
    jobs=json.load(open(sys.argv[1])); out=open(sys.argv[2],'a')
    with Pool(4) as p:
        for x in p.imap_unordered(job,jobs): out.write(json.dumps(x)+'\n'); out.flush()
