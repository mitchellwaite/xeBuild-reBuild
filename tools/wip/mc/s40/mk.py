import re,sys
s=open('H5b.c').read()
lo=s.index('for (i = 0; i < argc; i++) {'); hi=s.index('if (NO_MODE_ARG(mode, arg))')
loop=s[lo:hi]
def v(name, n, place):
    L=loop
    k=[0]
    def rep(m):
        k[0]+=1; return 'goto U%s;'%n
    L=L.replace('client_usage(%s, argv[i]);'%n,'goto U%s;'%n)
    if place=='in':   # at end of loop body
        idx=L.rindex('}'); L=L[:idx]+'if (0) { U%s: client_usage(%s, argv[i]); }\n\t'%(n,n)+L[idx:]
        t=s[:lo]+L+s[hi:]
    else:
        t=s[:lo]+L+'if (0) { U%s: client_usage(%s, argv[i]); }\n\t'%(n,n)+s[hi:]
    open(name,'w',newline='\n').write(t)
for n in '345':
    v('V%s_in.c'%n,n,'in'); v('V%s_out.c'%n,n,'out')
