# fixes for the byte check: case 6 forwarder (jump table entry), stale frequency for efail so the -w test isn't aligned
s=open('p2.c',newline='').read()
c='__asm__ goto ("" :::: c11); break;'; assert s.count(c)==1
open('b1.c','w',newline='\n').write(s.replace(c,'break;'))
ls=s.split('\n')
er=[i for i,x in enumerate(ls) if 'eerase:' in x][-1]
cp=lambda a:'__builtin_constant_p(block + %d)'%a
def fed(n,src):
    x=list(ls); k=x[er].index('log_printf'); x[er]=x[er][:k]+src+' '+x[er][k:]
    open(n+'.c','w',newline='\n').write('\n'.join(x).replace(c,'break;'))
fed('b2','if (%s) goto efail;'%cp(910))
fed('b3','if (%s && %s) goto efail;'%(cp(910),cp(911)))
fed('b4','if (%s && %s && %s) goto efail;'%(cp(910),cp(911),cp(912)))
fed('b5','if (%s && %s && %s && %s) goto efail;'%(cp(910),cp(911),cp(912),cp(913)))
