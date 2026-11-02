"""cur.py: current base (thenB d4 tree-only boost edge, no latch)."""
import sys; sys.path.insert(0,'.'); sys.path.insert(0,'../s53')
import rkgen
BE='	if (__builtin_constant_p(mode + 91) && __builtin_constant_p(mode + 92)) goto fkbo;\n'
def cond(d,o=91): return ' && '.join('__builtin_constant_p(mode + %d)'%(o+k) for k in range(d))
A='		if (__builtin_constant_p(mode + 93)) goto dtg;\n'
def base(d=4,o=91):
    s=rkgen.B.replace(BE,'',1); return s.replace(A,'		if (%s) goto fkbo;\n'%cond(d,o)+A,1)
A2='	dtg: if (E(reboot))\n		netReboot(reboot);\n	netDisconnect();'
def base2(npre=3,o=95):
    s=base()
    pre=''.join('	if (__builtin_constant_p(mode + %d)) goto ndl;\n'%(o+k) for k in range(npre))
    return s.replace(A2,pre+A2.replace('	netDisconnect();','	ndl: netDisconnect();'),1)
def bst(s,targets,where='then',o=60):
    """tree-only boosts: targets list of (label,depth); adds t4/t5 labels on the case 4/5 tests."""
    s=s.replace('			case 4:\n				if (cinfo','			case 4:\n				t4: if (cinfo',1).replace('			case 5:\n				if (cinfo','			case 5:\n				t5: if (cinfo',1)
    g=''.join('if (%s) goto %s; '%(cond(d,o+10*i),l) for i,(l,d) in enumerate(targets))
    if where=='then': s=s.replace(A,'		'+g+'\n'+A,1)
    elif where=='fail': s=s.replace('fail: __attribute__((cold));','fail: __attribute__((cold)); '+g,1)
    return s
def base3(npre=3,npost=0,dtgt='dtg',o=95):
    s=base2(npre,o)
    if npost: s=s.replace('	dtg: if (E(reboot))','	dtg: '+''.join('if (__builtin_constant_p(mode + %d)) goto ndl; '%(o+20+k) for k in range(npost))+'if (E(reboot))',1)
    if dtgt!='dtg': s=s.replace('if (__builtin_constant_p(mode + 93)) goto dtg;','if (__builtin_constant_p(mode + 93)) goto %s;'%dtgt,1)
    return s
