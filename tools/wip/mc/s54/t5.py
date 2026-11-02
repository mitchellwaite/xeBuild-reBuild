import sys,json; sys.path.insert(0,'.'); sys.path.insert(0,'../s53')
import rkgen,es2
FL=rkgen.FL
G={'1x21':[(FL,21)],'2':[(FL[:5],25),(FL[5:],26)],'3':[(FL[0:3],27),(FL[3:6],27),(FL[6:],27)],'9':[([l],29) for l in FL]}
for k,g in G.items():
    for w in (None,{},{'_ft':0}):
        if w=={'_ft':0}: w={}; o=['cdef']
        else: o=None
        r=es2.run(rkgen.mk2(w,g,order=o),'s54a'); print(k,w,o,r['es2'],r['per2'],r['score'])
