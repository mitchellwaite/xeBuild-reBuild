# single-label asm gotos at the -r head: keeps the loop PHI's low SSA version (partition leader), so the -i/-p tie stays
s=open('q0.c',newline='').read()
h='} else { k55l: if (!strnicmp(argv[i], "-r", 2)) {'; assert s.count(h)==1
g='if (({__asm__ goto("" :::: r5x, r3x); 0;}) || i + 1 == argc'; assert s.count(g)==1
M='__builtin_memset(argv, 0, kk); '
def A(lbl,tag,inp): return 'if (!kk) { %s: __attribute__((cold)); __asm__ goto ("" :%s: %s); } '%(tag,(': "a"(i) :' if inp else ':'),lbl)
def B(lbl,inp): return '__asm__ goto ("" :%s: %s); '%((': "a"(i) :' if inp else ':'),lbl)
V={}
for inp,ni in ((0,'n'),(1,'a')):
    V['s1'+ni]=M+A('r5x','ac',inp)+A('r3x','ad',inp)
    V['s2'+ni]=M+A('r3x','ac',inp)+A('r5x','ad',inp)
    V['s3'+ni]=M+'if (!kk) { ac: __attribute__((cold)); '+B('r5x',inp)+B('r3x',inp)+'} '
    V['s4'+ni]=M+'if (!kk) { ac: __attribute__((cold)); '+B('r3x',inp)+B('r5x',inp)+'} '
for n,x in V.items():
    a=s.replace(h,'} else { k55l: '+x+'if (!strnicmp(argv[i], "-r", 2)) {')
    open(n+'.c','w',newline='\n').write(a)
    open(n+'k.c','w',newline='\n').write(a.replace(g,'if (i + 1 == argc'))
