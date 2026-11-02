# early r5x/r3x edges AFTER the strnicmp call so the -r block keeps PRED_CALL (head block keeps its call)
s=open('z2.c',newline='').read()
h='} else { k55l: if (!strnicmp(argv[i], "-r", 2)) {'; assert s.count(h)==1
g='if (({__asm__ goto("" :::: r5x, r3x); 0;}) || i + 1 == argc'; assert s.count(g)==1
r3='{ r3x: client_usage(3, argv[i]); }'; r5='if (mode) { r5x: client_usage(5, argv[i]); }'
J='__asm__ goto ("" :::: r5x, r3x);'
n='} else { k55l: { int rr = strnicmp(argv[i], "-r", 2); '+J+' if (!rr) {'
# one extra closing brace needed: wrap by pre-declaring instead
n='} else { k55l: if (({ int rr = strnicmp(argv[i], "-r", 2); '+J+' !rr; })) {'
def w(a,x): open(a+'.c','w',newline='\n').write(x)
a=s.replace(h,n)
w('w1',a)
w('w2',a.replace(g,'if (i + 1 == argc'))
b=a.replace(r3,'{ r3x: __attribute__((cold)); client_usage(3, argv[i]); }').replace(r5,'if (mode) { r5x: __attribute__((cold)); client_usage(5, argv[i]); }')
w('w3',b)
w('w4',b.replace(g,'if (i + 1 == argc'))
