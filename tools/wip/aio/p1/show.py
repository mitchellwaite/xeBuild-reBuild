import sys,nm,sim3
TAG=sys.argv[1]; OV=eval(sys.argv[2]); ds=eval(sys.argv[3])
pre,g3,f3,g4,f4=sim3.load('../../../../build/v/aio_p1/%s/aio.bbro'%TAG)
G3={b:list(v) for b,v in g3.items()}; G4={b:list(v) for b,v in g4.items()}
n=0
for d in ds:
    n+=1;id_=9000+n
    if d[0]=='r3':
        l=G3.setdefault(d[1],[])
        l.insert(min(d[2],len(l)),('push',id_,d[3]) if d[3]>=-89 else ('ins','this',id_,d[3]))
    else:
        l=G4.setdefault(d[1],[]); l.insert(min(d[2],len(l)),('ins','this',id_,d[3]))
o3,o4=sim3.sim(pre,G3,G4,OV)
k=f4.index(74)
print(' '.join(nm.N.get(h,str(h)) for h in o4 if h<9000 and f4.index(h)>=k))
print(' '.join(nm.N.get(h,str(h)) for h in nm.REF4))
