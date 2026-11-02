import re
t=open('H5b.c').read()
lines=t.split('\n')
# loop region: lines 590..730 (1-based)
def sub(fn, rx, rep, lo=590, hi=730):
    L=list(lines)
    for k in range(lo-1,hi):
        L[k]=re.sub(rx,rep,L[k])
    open(fn,'w',newline='\n').write('\n'.join(L))
proto='void client_usage(int err, const char *arg) __attribute__((noreturn));'
# U1: __builtin_unreachable after every loop usage call
sub('U1.c', r'(client_usage\([^;]*\);)', r'{ \1 __builtin_unreachable(); }')
# U2: only usage(3)
sub('U2.c', r'(client_usage\(3[^;]*\);)', r'{ \1 __builtin_unreachable(); }')
# W1: static noinline noreturn wrapper for loop calls
w='static void __attribute__((noinline,noreturn)) cuw(int e, const char *a) { client_usage(e, a); }'
def wrap(fn, rx):
    L=list(lines)
    for k in range(589,730): L[k]=re.sub(rx, 'cuw(', L[k])
    s='\n'.join(L).replace(proto, proto+'\n'+w,1)
    open(fn,'w',newline='\n').write(s)
wrap('W1.c', r'client_usage\(')
wrap('W3.c', r'client_usage\((?=3)')
# F1: function pointer
f='static void (*volatile cufp)(int, const char *) = client_usage;'
L=list(lines)
for k in range(589,730): L[k]=re.sub(r'client_usage\((?=3)', 'cufp(', L[k])
open('F1.c','w',newline='\n').write('\n'.join(L).replace(proto, proto+'\n'+f,1))
