# dy: asm goto(dx) first, then the asm volatile block, so dx's edge isn't from the trace end (no boost)
for src,o in (('ua11','k1'),('ua12','k2'),('ub11','k3'),('ub12','k4')):
    s=open(src+'.c',newline='').read()
    a='dy: asm volatile(""); __asm__ goto ("" :::: dx); '; assert s.count(a)==1
    open(o+'y.c','w',newline='\n').write(s.replace(a,'dy: __asm__ goto ("" :::: dx); asm volatile(""); '))
