import sys,json; sys.path.insert(0,'.'); sys.path.insert(0,'../s53')
import rkgen,es2,cur
for v in ('mode','reboot','i','argc','(int)start','(int)ip'):
  for d in (1,2):
    s=cur.base()
    a='	dtg: if (E(reboot))\n		netReboot(reboot);\n	netDisconnect();'
    c=' && '.join('__builtin_constant_p(%s + %d)'%(v,95+k) for k in range(d))
    b='	if (%s) goto ndl;\n'%c+a.replace('	netDisconnect();','	ndl: netDisconnect();')
    s=s.replace(a,b,1)
    r=es2.run(rkgen.mk({},base=s),'s54c'); print(v,d,r['es2'],r['per2'],r['score'],flush=True)
