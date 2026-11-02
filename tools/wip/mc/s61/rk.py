import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s53')); import es2,es,hsim
p=os.path.join(es.R,'build','mcmatch','slotm') if sys.argv[1]=='m' else os.path.join(es.R,'build','v','mc42','slot_'+sys.argv[1])
Rr,keys=hsim.load(p); r=Rr[int(sys.argv[2])-1]
print('pre',r['pre'])
for b,e in r['g'].items(): print(b,e)
