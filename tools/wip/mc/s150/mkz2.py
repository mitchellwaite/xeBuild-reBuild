s=open('z3p.c',newline='').read()
f='if ((char *)__builtin_constant_p(i + 30) == (char *)1 && (char *)__builtin_constant_p(i + 31) == (char *)1) goto k55l;'; assert s.count(f)==1
g='if (({__asm__ goto("" :::: r5x, r3x); 0;}) || i + 1 == argc'; assert s.count(g)==1
open('z7.c','w',newline='\n').write(s.replace(f,''))
open('z8.c','w',newline='\n').write(s.replace(f,'').replace(g,'if (i + 1 == argc'))
# same without the asm at the head, to see what the feeder does on its own
b=open('z2.c',newline='').read()
open('z9.c','w',newline='\n').write(b.replace(f,''))
