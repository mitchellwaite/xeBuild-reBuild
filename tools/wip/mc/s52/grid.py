import sys,os,json,itertools
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import ck3, es, lp3
BC='__builtin_constant_p(mode + %d)'
def back(src, cond, where):
    src=src.replace('\t} else {\n\t\tif (netConnect(ip)) {','\t} else {\n\t\tfkbo: if (netConnect(ip)) {',1)
    if where=='fkN': return src.replace('fkN: ;','fkN: if (%s) goto fkbo;'%cond,1)
    if where=='tail': return src.replace('\tif (E(reboot))\n','\tif (%s) goto fkbo;\n\tif (E(reboot))\n'%cond,1)
    if where=='gi': return src.replace('\t\t\tcinfo = netGetInfo();\n\t\t\tswitch','\t\t\tcinfo = netGetInfo();\n\t\t\tif (%s) goto fkbo;\n\t\t\tswitch'%cond,1)
def mk(sp,k1,k2,b):
    s=ck3.var(sp,k1,k2)
    if b=='none': return s
    if b[0] in 'fq': return lp3.V[b](s)
    w,d=b.split(':'); cond=' && '.join(BC%(91+k) for k in range(int(d)))
    return back(s,cond,w)
if __name__=='__main__':
    log=open('grid.jsonl','a')
    splits=[(9,21,0),(5,25,26),(4,26,25),(6,24,27),(3,27,24),(9,10,0)]
    boosts=['none','f1','f2','q0','fkN:1','tail:1','gi:1','tail:2']
    for (sp,k1,k2),b in itertools.product(splits,boosts):
        tag='s52g_%d_%d_%d_%s'%(sp,k1,k2,b.replace(':','_'))
        try: r=es.run(mk(sp,k1,k2,b),tag,fncmp=False)
        except Exception as e: r={'err':repr(e)}
        d={'sp':sp,'k1':k1,'k2':k2,'b':b,'r':r}; print(json.dumps(d),flush=True); log.write(json.dumps(d)+'\n'); log.flush()
