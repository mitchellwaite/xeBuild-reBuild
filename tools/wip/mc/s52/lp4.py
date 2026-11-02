import sys,os,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import ck3, es
BC='__builtin_constant_p(mode + %d)'
def mk(sp,k1,k2,where,d,hdr):
    s=ck3.var(sp,k1,k2)
    cond=' && '.join(BC%(91+k) for k in range(d))
    if hdr=='A': s=s.replace('{ struct {} fko;','fkbo: { struct {} fko;',1)
    if hdr=='G': s=s.replace('fkN: ;','fkN: fkbo: ;',1)
    if where=='gi': s=s.replace('\t\t\tcinfo = netGetInfo();\n\t\t\tswitch','\t\t\tcinfo = netGetInfo();\n\t\t\tif (%s) goto fkbo;\n\t\t\tswitch'%cond,1)
    if where=='tail': s=s.replace('\tif (E(reboot))\n','\tif (%s) goto fkbo;\n\tif (E(reboot))\n'%cond,1)
    return s
if __name__=='__main__':
    for a in sys.argv[1:]:
        sp,k1,k2,w,d,h=a.split(','); 
        tag='s52h_'+a.replace(',','_')
        r=es.run(mk(int(sp),int(k1),int(k2),w,int(d),h),tag,fncmp=False)
        tr=[l.split(':')[1].strip() for l in open(os.path.join(es.R,'build','v','mc42','slot_'+tag,'bbro_mc.txt')) if l.startswith('Trace') and '(round 2)' in l] if r else []
        print(a,r,tr[:5],flush=True)
