import sys,json; sys.path.insert(0,'.'); sys.path.insert(0,'../s53')
import rkgen,es2
BE='	if (__builtin_constant_p(mode + 91) && __builtin_constant_p(mode + 92)) goto fkbo;\n'
def cond(d,o=91): return ' && '.join('__builtin_constant_p(mode + %d)'%(o+k) for k in range(d))
P={'thenA':('		if (__builtin_constant_p(mode + 93)) goto dtg;\n','		if (__builtin_constant_p(mode + 93)) goto dtg;\n		if (%s) goto fkbo;\n'),
   'thenB':('		if (__builtin_constant_p(mode + 93)) goto dtg;\n','		if (%s) goto fkbo;\n		if (__builtin_constant_p(mode + 93)) goto dtg;\n'),
   'reb':('			if (netConnect(ip)) {\n			rok:','			if (%s) goto fkbo;\n			if (netConnect(ip)) {\n			rok:'),
   'u2':('{ AT(u2) client_usage(2, NULL); }','{ if (%s) goto fkbo; AT(u2) client_usage(2, NULL); }'),
}
res=[]
for k,(a,b) in P.items():
  for d in (1,2,3,4):
    s=rkgen.B.replace(BE,'',1); assert a in s; s=s.replace(a,b%cond(d),1)
    for w in (None,{}):
        r=es2.run(s if w is None else rkgen.mk(w,base=s),'s54a'); print(k,d,'J' if w is not None else '-',r['es2'],r['per2'],r['score'],flush=True)
