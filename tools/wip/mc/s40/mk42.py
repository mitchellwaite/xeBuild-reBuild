import re,itertools
t=open('H5b.c').read()
pat=re.compile(r'if \((.*)\)\n(\t+)client_usage\(3, argv\[i\]\);')
ms=list(pat.finditer(t))
def make(sel,val):
    s=t
    for n in sorted(sel,reverse=True):
        m=ms[n]
        s=s[:m.start()]+'if (__builtin_expect(!(%s),%d)) ; else\n%sclient_usage(3, argv[i]);'%(m.group(1),val,m.group(2))+s[m.end():]
    return s
out=[]
for r in (2,3):
    for sel in itertools.combinations(range(4,8),r):
        fn='C%s.c'%''.join(map(str,sel)); open(fn,'w',newline='\n').write(make(sel,1)); out.append(fn)
for n in range(8):
    fn='Z%d.c'%n; open(fn,'w',newline='\n').write(make([n],0)); out.append(fn)
print(' '.join(out))
