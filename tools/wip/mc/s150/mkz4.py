s=open('z2.c',newline='').read()
c='AT(c10)JMP(c10);'; assert s.count(c)==1
r3='{ r3x: client_usage(3, argv[i]); }'; r5='if (mode) { r5x: client_usage(5, argv[i]); }'
def w(a,x): open(a+'.c','w',newline='\n').write(x)
a=s.replace(c,'AT(c10)JMP(c10); __asm__ goto ("" :::: r5x, r3x);')
w('v1',a)
b=a.replace(r3,'{ r3x: __attribute__((cold)); client_usage(3, argv[i]); }').replace(r5,'if (mode) { r5x: __attribute__((cold)); client_usage(5, argv[i]); }')
w('v2',b)
w('v3',s.replace(c,'AT(c10)JMP(c10,r5x,r3x);'))
