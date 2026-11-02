"""raw.py slot|m: print canonical B id -> raw block id map for R3 ids."""
import sys,os,re
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s53')); import es2,es,hsim
p=os.path.join(es.R,'build','mcmatch','slotm') if sys.argv[1]=='m' else os.path.join(es.R,'build','v','mc42','slot_'+sys.argv[1])
Rr,keys=hsim.load(p); mp={}
for r in Rr:
    for x in r['pre']+[y for e in r['g'].values() for y in e]: pass
T=[]
for ri,r in enumerate(Rr,1):
    t=['pre']+[('%s%s'%(x[0][0],x[1]) if x[0]!='ins' else 'i%s:%s'%(x[2],x[1][0])) for x in r['pre']]
    for b,e in r['g'].items():
        t.append('G%s'%b); t+=[('%s%s'%(x[0][0],x[1]) if x[0]!='ins' else 'i%s:%s'%(x[2],x[1][0])) for x in e]
    for x in t:
        m=re.match(r'^(\D+)(\d+)',x)
        if m: mp.setdefault(int(m.group(2)),len(mp))
inv={v:k for k,v in mp.items()}
print(' '.join('B%d=%d'%(i,inv[i]) for i in range(55,100) if i in inv))
