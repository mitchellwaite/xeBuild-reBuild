# head asm goto before the strnicmp with "a"(i) (i is in eax there in the reference) and a dead side-effect
# call (memset of constant_p bytes, folded at fab) so PRED_CALL still fires on the -ip test
s=open('z2.c',newline='').read()
h='} else { k55l: if (!strnicmp(argv[i], "-r", 2)) {'; assert s.count(h)==1
g='if (({__asm__ goto("" :::: r5x, r3x); 0;}) || i + 1 == argc'; assert s.count(g)==1
M='__builtin_memset(dummy, 0, __builtin_constant_p(i + 8800)); '
def w(a,x): open(a+'.c','w',newline='\n').write(x)
for n,J in (('n','__asm__ goto ("" :::: r5x, r3x); '),('a','__asm__ goto ("" :: "a"(i) :: r5x, r3x); ')):
    a=s.replace(h,'} else { k55l: '+M+J+'if (!strnicmp(argv[i], "-r", 2)) {')
    w('u1'+n,a); w('u2'+n,a.replace(g,'if (i + 1 == argc'))
    a=s.replace(h,'} else { '+M+J+'k55l: if (!strnicmp(argv[i], "-r", 2)) {')
    w('u3'+n,a); w('u4'+n,a.replace(g,'if (i + 1 == argc'))
