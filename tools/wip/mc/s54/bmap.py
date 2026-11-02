"""bmap.py: es2-canonical B map for a slot (B index -> raw bb id), same rule as s53/es2.toks."""
import sys,os,re
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s53')); import es2,es,hsim
def bm(slot):
    Rr,keys=hsim.load(slot); out=[]
    for r in Rr:
        out+=[('%s%s'%(x[0][0],x[1]) if x[0]!='ins' else 'i%s:%s'%(x[2],x[1][0])) for x in r['pre']]
        for b,e in r['g'].items():
            out.append('G%s'%b); out+=[('%s%s'%(x[0][0],x[1]) if x[0]!='ins' else 'i%s:%s'%(x[2],x[1][0])) for x in e]
    mp={}
    for x in out:
        m=re.match(r'^(\D+)(\d+)',x); mp.setdefault(int(m.group(2)),len(mp))
    return {v:k for k,v in mp.items()}
MS=os.path.join(es.R,'build','mcmatch','slotm')
def slot(tag): return os.path.join(es.R,'build','v','mc42','slot_'+tag)
if __name__=='__main__':
    a=bm(MS); b=bm(slot(sys.argv[1]))
    for k in sorted(set(a)|set(b)):
        if len(sys.argv)<3 or k in map(int,sys.argv[2].split(',')): print('B%d m%s t%s'%(k,a.get(k),b.get(k)))
