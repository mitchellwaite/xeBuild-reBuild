# the partition of the loop i gets its pseudo in expand_used_vars only if its lowest-version member has a decl:
# give the increment a named temporary
s=open('r1.c',newline='').read()
a='for (i = 0; i < argc; i++) {'; print(s.count(a))
b=[p for p in range(len(s)) if s.startswith(a,p)][-1]
def rep(new): return s[:b]+new+s[b+len(a):]
open('n1.c','w',newline='\n').write(rep('for (i = 0; i < argc; ({ int ni = i + 1; i = ni; })) {'))
open('n2.c','w',newline='\n').write(rep('for (i = 0; i < argc; ({ int i32 = i; i = i32 + 1; })) {'))
c='int kk = __builtin_constant_p(argc);'
x=rep('for (i = 0; i < argc; i = j) { j = i + 1; ').replace(c,c)
open('n3.c','w',newline='\n').write(rep('for (i = 0; i < argc; ({ j = i + 1; i = j; })) {'))
