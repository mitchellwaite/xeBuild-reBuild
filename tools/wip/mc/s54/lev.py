"""lev.py: full lever text builder on c_r10 (s54 levers). st keys:
 w   rok fake weights {label:n, '_ft':n}      fk  fkbo fakes moved from ft to a fkbo label {label:n}
 B   tree-only boosts from fail {label:d}      X   exit diversions to ndl right after a case label {label:d}
 npre ndl diversions before dtg (default 3)    dd  depth of the then-branch fkbo boost (default 4)
 dt  depth of the then-branch dtg diversion (default 1)"""
import sys,os
D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D)
import rkgen
B0=rkgen.B
LAB=['c12','c3','c1','t4','t5','c8','c2','c9','c10','c11','c7','cdef']
def cond(d,o): return ' && '.join('__builtin_constant_p(mode + %d)'%(o+k) for k in range(d))
def text(st):
    s=B0
    s=s.replace('	if (__builtin_constant_p(mode + 91) && __builtin_constant_p(mode + 92)) goto fkbo;\n','',1)
    A='		if (__builtin_constant_p(mode + 93)) goto dtg;\n'
    s=s.replace(A,'		if (%s) goto fkbo;\n'%cond(st.get('dd',4),91)+'		if (%s) goto dtg;\n'%cond(st.get('dt',1),130),1)
    A2='	dtg: if (E(reboot))\n		netReboot(reboot);\n	netDisconnect();'
    pre=''.join('	if (__builtin_constant_p(mode + %d)) goto ndl;\n'%(95+k) for k in range(st.get('npre',3)))
    s=s.replace(A2,pre+A2.replace('	netDisconnect();','	ndl: netDisconnect();'),1)
    s=s.replace('			case 4:\n				if (cinfo','			case 4:\n				AT(t4) if (cinfo',1).replace('			case 5:\n				if (cinfo','			case 5:\n				AT(t5) if (cinfo',1)
    for i,(l,d) in enumerate(sorted(st.get('X',{}).items())):
        if d: a='AT(%s) '%l; assert s.count(a)==1,l; s=s.replace(a,a+'if (%s) goto ndl; '%cond(d,400+10*i),1)
    g=''.join('if (%s) goto %s; '%(cond(d,200+10*i),l) for i,(l,d) in enumerate(sorted(st.get('B',{}).items())) if d)
    if g: s=s.replace('fail: __attribute__((cold));','fail: __attribute__((cold)); '+g,1)
    if st.get('fk'):
        s=s.replace(rkgen.FOLD,fkw(st['fk']),1)
    return rkgen.mk(st.get('w',{}),base=s)
def fkw(fk):
    reals=rkgen.FL; ft=21-sum(fk.values()); labs=list(reals); body=''; outer=''
    tg=['fqE']*ft+[l for l in reals for _ in range(fk.get(l,0))]
    for j,t in enumerate(tg): labs.append('fq%d'%j); body+='fq%d: goto ofq%d; '%(j,j); outer+='ofq%d: goto %s; '%(j,t)
    return 'fkbo: { struct {} fqo; { struct {} fqv; __asm__ ("" :: "X"(&fqo), "X"(&fqv)); __asm__ goto ("" :::: %s); goto fqn; %s} fqn: ; goto fqE; %s} fqE: ;'%(', '.join(labs),body,outer)
