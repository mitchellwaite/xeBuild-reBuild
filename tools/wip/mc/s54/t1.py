import sys,json; sys.path.insert(0,'.')
sys.path.insert(0,'../s53'); import rkgen,es2
B0=rkgen.B
BE='	if (__builtin_constant_p(mode + 91) && __builtin_constant_p(mode + 92)) goto fkbo;\n'
V={
 'mv_after_fkN': [(BE,''),('fkM: ; } fkN: ;','fkM: ; } fkN: if (__builtin_constant_p(mode + 91) && __builtin_constant_p(mode + 92)) goto fkbo;')],
 'mv_fkA2': [(BE,''),('fkA2: goto fkN;','fkA2: if (__builtin_constant_p(mode + 91) && __builtin_constant_p(mode + 92)) goto fkbo; goto fkN;')],
 'mv_after_gi': [(BE,''),('fkM: ; } fkN: ;\n			cinfo = netGetInfo();','fkM: ; } fkN: ;\n			cinfo = netGetInfo(); if (__builtin_constant_p(mode + 91) && __builtin_constant_p(mode + 92)) goto fkbo;')],
}
def app(s,subs):
    for a,b in subs: assert a in s,a; s=s.replace(a,b,1)
    return s
for k,subs in V.items():
    for w in ({},None):
        base=app(B0,subs)
        txt=base if w is None else rkgen.mk(w,base=base)
        r=es2.run(txt,'s54a'); print(k,'JMP' if w is not None else 'noJMP',r['es2'],r['per2'],r['score'])
