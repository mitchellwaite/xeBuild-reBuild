"""es2.py: es with ALL block ids canonicalized by first appearance over the whole history (rounds 1..4 in order),
so blocks numbered differently (e.g. 109 vs an anonymous >=1000 id) count as equal when the event sequence is."""
import sys,os,re,io,contextlib
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s51')); import es, hsim
def toks(slot):
    Rr,keys=hsim.load(slot); out={}
    for ri,r in enumerate(Rr,1):
        t=['pre']+[('%s%s'%(x[0][0],x[1]) if x[0]!='ins' else 'i%s:%s'%(x[2],x[1][0])) for x in r['pre']]
        for b,e in r['g'].items():
            t.append('G%s'%b); t+=[('%s%s'%(x[0][0],x[1]) if x[0]!='ins' else 'i%s:%s'%(x[2],x[1][0])) for x in e]
        out[ri]=t
    mp={}
    def cn(m): return m.group(1)+'B%d'%mp.setdefault(int(m.group(2)),len(mp))
    return {r:[re.sub(r'^(\D+)(\d+)',cn,x) for x in out[r]] for r in sorted(out)}
M=toks(os.path.join(es.R,'build','mcmatch','slotm'))
def escore(slot):
    T=toks(slot); per={r:es.dist(M.get(r,[]),T.get(r,[])) for r in set(M)|set(T)}
    return sum(es.W.get(r,1)*d for r,d in per.items()),per
def run(text,tag,fncmp=False):
    r=es.run(text,tag,fncmp)
    if r is None: return None
    try: r['es2'],r['per2']=escore(os.path.join(es.R,'build','v','mc42','slot_'+tag))
    except Exception as e: r['es2'],r['per2']=9999,repr(e)
    return r
if __name__=='__main__':
    if sys.argv[1].endswith('.c'): print(run(open(sys.argv[1]).read(),sys.argv[2],True))
    else: print(escore(os.path.join(es.R,'build','v','mc42','slot_'+sys.argv[1])))
