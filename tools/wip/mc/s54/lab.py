import sys,os,re; sys.path.insert(0,'.')
import run,r3,rkgen,es
for l in rkgen.RL:
    r=run.ev({l:14},'s54L')
    o=r3.show(os.path.join(es.R,'build','v','mc42','slot_s54L'),3)
    i=[k for k,x in enumerate(o) if 'rok' in x][0]
    seg=[x for x in o[i+1:i+14] if x.startswith(('Cha','sta'))]
    # find best prio
    best=max(seg,key=lambda x:-int(x.split()[-1]) if x.startswith('Cha') else 0)
    print(l,r['per2'],best)
