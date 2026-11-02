s=open('z2.c',newline='').read()
d='dz: asm volatile("#");'; assert s.count(d)==1
s=s.replace(d,'dz: asm volatile("" : : : "cc");')
h='} else { k55l: if (!strnicmp(argv[i], "-r", 2)) {'; assert s.count(h)==1
g='if (({__asm__ goto("" :::: r5x, r3x); 0;}) || i + 1 == argc'; assert s.count(g)==1
def w(a,x): open(a+'.c','w',newline='\n').write(x)
w('q0',s)
Mi='__builtin_memset(dummy, 0, __builtin_constant_p(i + 8800)); '
Mk='__builtin_memset(dummy, 0, kk); '
Ji='__asm__ goto ("" :: "a"(i) :: r5x, r3x); '; Jn='__asm__ goto ("" :::: r5x, r3x); '
Ai=lambda J:'if (!__builtin_constant_p(i + 8801)) { ac: __attribute__((cold)); '+J+'} '
Ak=lambda J:'if (!kk) { ac: __attribute__((cold)); '+J+'} '
Al=lambda J:'if (!__builtin_constant_p(mode + 8801)) { ac: __attribute__((cold)); '+J+'} '
n=0
for mn,M in (('i',Mi),('k',Mk)):
  for jn,J in (('a',Ji),('n',Jn)):
    for an,A in (('i',Ai),('k',Ak),('l',Al)):
      for kn,kp in (('1',1),('2',0)):
        x=s.replace(h,'} else { k55l: '+M+A(J)+'if (!strnicmp(argv[i], "-r", 2)) {')
        if not kp: x=x.replace(g,'if (i + 1 == argc')
        w('q'+mn+jn+an+kn,x)
