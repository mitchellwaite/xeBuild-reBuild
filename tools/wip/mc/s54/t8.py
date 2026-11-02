import sys,json; sys.path.insert(0,'.'); sys.path.insert(0,'../s53')
import rkgen,es2,cur,fq
A='	dtg: if (E(reboot))\n		netReboot(reboot);\n	netDisconnect();'
def var(npre,npost,o=95):
    s=cur.base()
    pre=''.join('	if (__builtin_constant_p(mode + %d)) goto ndl;\n'%(o+k) for k in range(npre))
    post=''.join('if (__builtin_constant_p(mode + %d)) goto ndl; '%(o+10+k) for k in range(npost))
    b=pre+A.replace('dtg: if (E(reboot))','dtg: '+post+'if (E(reboot))').replace('	netDisconnect();','	ndl: netDisconnect();')
    return s.replace(A,b,1)
if __name__=='__main__':
  for npre in (0,1,2,3):
    for npost in (0,1,2):
        s=rkgen.mk({},base=var(npre,npost))
        b,t=fq.fq(s,'t8'); P=fq.parse(t); f=P[142][0]
        r=es2.run(s,'s54c'); print(npre,npost,'nr',f,r['es2'],r['per2'],r['score'],flush=True)
