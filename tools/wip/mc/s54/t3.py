import sys,json; sys.path.insert(0,'.'); sys.path.insert(0,'../s53')
import rkgen,es2
BE='if (__builtin_constant_p(mode + 91) && __builtin_constant_p(mode + 92)) goto fkbo;'
C={'1':'if (__builtin_constant_p(mode + 91)) goto fkbo;',
   '2x':BE+' '+BE.replace('91','94').replace('92','95'),
   '1+2':BE+' if (__builtin_constant_p(mode + 94)) goto fkbo;',
   '3':'if (__builtin_constant_p(mode + 91) && __builtin_constant_p(mode + 92) && __builtin_constant_p(mode + 94)) goto fkbo;',
   'or':'if (__builtin_constant_p(mode + 91) || __builtin_constant_p(mode + 92)) goto fkbo;',
   'E1':'if (__builtin_expect(__builtin_constant_p(mode + 91),1)) goto fkbo;',
}
for k,v in C.items():
    b=rkgen.B.replace(BE,v,1)
    for w in (None,{}):
        t=b if w is None else rkgen.mk(w,base=b)
        r=es2.run(t,'s54a'); print(k,'J' if w is not None else '-',r['es2'],r['per2'],r['score'])
