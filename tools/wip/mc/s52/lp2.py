import sys,os,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import ck3, es
BC='__builtin_constant_p(mode + %d)'
CONDS={
 'b': BC%91,
 'bb': BC%91+' && '+BC%92,
 'bbb': BC%91+' && '+BC%92+' && '+BC%93,
 'bd': BC%91+' && arg == dummy',
 'bnd': BC%91+' && arg != dummy',
 'bz': BC%91+' && !cinfo',
 'bi': BC%91+' && i == 7',
 'bm': BC%91+' && mode == 7',
 'bmn': BC%91+' && mode != 7',
 'br': BC%91+' && reboot',
 'bnr': BC%91+' && !reboot',
}
def loop(src, cond, where='fkN: ;'):
    src=src.replace('\t} else {\n\t\tif (netConnect(ip)) {','\t} else {\n\t\tfkbo: if (netConnect(ip)) {',1)
    return src.replace(where, where+' if (%s) goto fkbo;'%cond,1)
if __name__=='__main__':
    sp,k1,k2=[int(x) for x in sys.argv[1].split(',')]
    for c in sys.argv[2:]:
        t=loop(ck3.var(sp,k1,k2),CONDS[c])
        r=es.run(t,'s52m_%s_%s'%(sys.argv[1].replace(',','_'),c),fncmp=False); print(sys.argv[1],c,r,flush=True)
