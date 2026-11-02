s=open('H5b.c').read()
open('N0.c','w',newline='\n').write(s.replace('void client_usage(int err, const char *arg) __attribute__((noreturn));','void client_usage(int err, const char *arg);',1))
open('N1.c','w',newline='\n').write(s.replace('__attribute__((noreturn));','__attribute__((noreturn,cold));',1))
lo=s.index('for (i = 0; i < argc; i++) {'); hi=s.index('if (NO_MODE_ARG(mode, arg))')
L=s[lo:hi]; idx=[]; p=0
while True:
    p=L.find('client_usage(3, argv[i]);',p)
    if p<0: break
    idx.append(p); p+=1
print(len(idx))
# pair-share: site k jumps to site k+1's call
for k in range(len(idx)-1):
    a,b=idx[k],idx[k+1]
    t=L[:a]+'goto P3;'+L[a+len('client_usage(3, argv[i]);'):b]+'P3: client_usage(3, argv[i]);'+L[b+len('client_usage(3, argv[i]);'):]
    open('Q%d.c'%k,'w',newline='\n').write(s[:lo]+t+s[hi:])
    t=L[:a]+'P3: client_usage(3, argv[i]);'+L[a+len('client_usage(3, argv[i]);'):b]+'goto P3;'+L[b+len('client_usage(3, argv[i]);'):]
    open('R%d.c'%k,'w',newline='\n').write(s[:lo]+t+s[hi:])
