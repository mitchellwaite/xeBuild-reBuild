# as mkz5 + the asm goto in a cold arm of a folded test so r3x/r5x keep frequency 0 (key 0)
s=open('z2.c',newline='').read()
h='} else { k55l: if (!strnicmp(argv[i], "-r", 2)) {'; assert s.count(h)==1
g='if (({__asm__ goto("" :::: r5x, r3x); 0;}) || i + 1 == argc'; assert s.count(g)==1
r3='{ r3x: client_usage(3, argv[i]); }'; r5='if (mode) { r5x: client_usage(5, argv[i]); }'
M='__builtin_memset(dummy, 0, __builtin_constant_p(i + 8800)); '
def w(a,x): open(a+'.c','w',newline='\n').write(x)
for n,J in (('n','__asm__ goto ("" :::: r5x, r3x); '),('a','__asm__ goto ("" :: "a"(i) :: r5x, r3x); ')):
    A='if (!__builtin_constant_p(i + 8801)) { ac: __attribute__((cold)); '+J+'} '
    a=s.replace(h,'} else { k55l: '+M+A+'if (!strnicmp(argv[i], "-r", 2)) {')
    w('t1'+n,a); w('t2'+n,a.replace(g,'if (i + 1 == argc'))
    c=s.replace(r3,'{ r3x: __attribute__((cold)); client_usage(3, argv[i]); }').replace(r5,'if (mode) { r5x: __attribute__((cold)); client_usage(5, argv[i]); }')
    a=c.replace(h,'} else { k55l: '+M+J+'if (!strnicmp(argv[i], "-r", 2)) {')
    w('t3'+n,a); w('t4'+n,a.replace(g,'if (i + 1 == argc'))
