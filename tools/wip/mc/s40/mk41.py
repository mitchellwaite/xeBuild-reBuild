import re
t=open('H5b.c').read()
# I*: invert "if (COND)\n\t\t\t\tclient_usage(3, argv[i]);" into "if (!(COND)) ; else client_usage(...)"
pat=re.compile(r'if \((.*)\)\n(\t+)client_usage\(3, argv\[i\]\);')
ms=list(pat.finditer(t))
print(len(ms))
for n,m in enumerate(ms):
    s=t[:m.start()]+'if (__builtin_expect(!(%s),1)) ; else\n%sclient_usage(3, argv[i]);'%(m.group(1),m.group(2))+t[m.end():]
    open('I%d.c'%n,'w',newline='\n').write(s)
    s=t[:m.start()]+'if (!(%s)) goto ok%d;\n%sclient_usage(3, argv[i]);\n%sok%d:;'%(m.group(1),n,m.group(2),m.group(2),n)+t[m.end():]
    open('G%d.c'%n,'w',newline='\n').write(s)
