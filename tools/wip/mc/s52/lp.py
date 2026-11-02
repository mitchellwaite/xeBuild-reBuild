import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import ck3, es
def loop(src, n=1, where='fkN'):
    g=' '.join('if (__builtin_constant_p(mode + %d)) goto fkbo;'%(91+k) for k in range(n))
    src=src.replace('\t} else {\n\t\tif (netConnect(ip)) {','\t} else {\n\t\tfkbo: if (netConnect(ip)) {',1)
    src=src.replace('fkN: ;','fkN: '+g,1)
    return src
if __name__=='__main__':
    for a in sys.argv[1:]:
        sp,k1,k2,n=[int(x) for x in a.split(',')]
        t=loop(ck3.var(sp,k1,k2),n)
        r=es.run(t,'s52l%s'%a.replace(',','_'),fncmp=False); print(a,r,flush=True)
