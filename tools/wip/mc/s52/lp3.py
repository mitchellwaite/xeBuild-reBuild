import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import ck3, es
BC='__builtin_constant_p(mode + %d)'
def fwd(src, depth):
    g=''.join('if (%s) '%(BC%(77+k)) for k in range(depth))+'goto fkbo;\n\t'
    src=src.replace('\tif (NO_MODE_ARG(mode, arg)) {','\t'+g+'if (NO_MODE_ARG(mode, arg)) {',1)
    return src.replace('\t} else {\n\t\tif (netConnect(ip)) {','\t} else {\n\t\tfkbo: if (netConnect(ip)) {',1)
def q(src, n):
    src=src.replace('\t} else {\n\t\tif (netConnect(ip)) {','\t} else {\n\t\tint fkq = 0; fkbo: if (netConnect(ip)) {',1)
    return src.replace('fkN: ;','fkN: if (%s) { if (fkq++ < %d) goto fkbo; }'%(BC%91,n),1)
V={'f1':lambda s:fwd(s,1),'f2':lambda s:fwd(s,2),'f3':lambda s:fwd(s,3),'f4':lambda s:fwd(s,4),
   'q1':lambda s:q(s,1),'q2':lambda s:q(s,2),'q0':lambda s:q(s,0)}
if __name__=='__main__':
    sp,k1,k2=[int(x) for x in sys.argv[1].split(',')]
    for c in sys.argv[2:]:
        t=V[c](ck3.var(sp,k1,k2))
        tag='s52n_%s_%s'%(sys.argv[1].replace(',','_'),c)
        r=es.run(t,tag,fncmp=False); 
        tr=[l.strip() for l in open(os.path.join(es.R,'build','v','mc42','slot_'+tag,'bbro_mc.txt')) if l.startswith('Trace') and '(round 2)' in l]
        print(sys.argv[1],c,r,tr[:5],flush=True)
