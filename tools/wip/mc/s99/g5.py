import sys
K='if (__builtin_constant_p(i + 5555)) goto k61l;'
for b,t in (('H1.c','h'),('J1.c','j'),('m02n.c','m')):
  s=open(b).read(); assert s.count(K)==1
  for n in range(1,6):
    c=''.join(' && __builtin_constant_p(i + %d)'%(77780+j) for j in range(n))
    open('k%d%s.c'%(n,t),'w',newline='\n').write(s.replace(K,'if (__builtin_constant_p(i + 5555)%s) goto k61l;'%c))
