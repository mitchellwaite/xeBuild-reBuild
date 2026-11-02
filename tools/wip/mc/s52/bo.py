import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import ck3, es
def boost(src, n=1, cond='__builtin_constant_p(mode + %d)'):
    g=''.join('if (%s) goto fkbo;\n\t'%(cond%(77+k)) for k in range(n))
    src=src.replace('\tif (NO_MODE_ARG(mode, arg)) {','\t'+g+'if (NO_MODE_ARG(mode, arg)) {',1)
    src=src.replace('\t} else {\n\t\tif (netConnect(ip)) {','\t} else {\n\t\tfkbo: if (netConnect(ip)) {',1)
    return src
if __name__=='__main__':
    for a in sys.argv[1:]:
        sp,k1,k2,n=[int(x) for x in a.split(',')]
        t=boost(ck3.var(sp,k1,k2),n) if sp else boost(ck3.B,n)
        r=es.run(t,'s52b%s'%a.replace(',','_'),fncmp=False); print(a,r,flush=True)
