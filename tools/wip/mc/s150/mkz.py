# mkz.py : variants on z1: distinct dz (asm comment) + r5x/r3x asm goto before the -r test
s=open('z1.c',newline='').read()
d='dz: asm volatile("");'; assert s.count(d)==1
s=s.replace(d,'dz: asm volatile("#");')
open('z2.c','w',newline='\n').write(s)
h='} else { k55l: if (!strnicmp(argv[i], "-r", 2)) {'; assert s.count(h)==1
g='if (({__asm__ goto("" :::: r5x, r3x); 0;}) || i + 1 == argc'; assert s.count(g)==1
r3='{ r3x: client_usage(3, argv[i]); }'; assert s.count(r3)==1
r5='if (mode) { r5x: client_usage(5, argv[i]); }'; assert s.count(r5)==1
J='__asm__ goto ("" :::: r5x, r3x);'
c3='{ r3x: __attribute__((cold)); client_usage(3, argv[i]); }'
c5='if (mode) { r5x: __attribute__((cold)); client_usage(5, argv[i]); }'
def w(n,x): open(n+'.c','w',newline='\n').write(x)
for cn,cold in (('p',0),('c',1)):
    t=s.replace(r3,c3).replace(r5,c5) if cold else s
    w('z3'+cn,t.replace(h,'} else { k55l: '+J+' if (!strnicmp(argv[i], "-r", 2)) {'))
    w('z4'+cn,t.replace(h,'} else { '+J+' k55l: if (!strnicmp(argv[i], "-r", 2)) {'))
    w('z5'+cn,t.replace(h,'} else { k55l: '+J+' if (!strnicmp(argv[i], "-r", 2)) {').replace(g,'if (i + 1 == argc'))
    w('z6'+cn,t.replace(h,'} else { '+J+' k55l: if (!strnicmp(argv[i], "-r", 2)) {').replace(g,'if (i + 1 == argc'))
