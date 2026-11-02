# gen6.py: split the -keys arm with a never-taken asm goto so its body freq drops below round-3 exec_th
import os
s = open('b18.c').read()
K = '} else if (!strnicmp(argv[i], "-keys", 5)) {'
n = 0
for t in ('k55l', 'k61l', 'k67l', 'u2', 'wb3', 'r3x', 'r5x', 'w5x', 'lu1', 'cdef', 'fail', 'dtg', 'ndl', 'c3', 'dsp', 'fkbo'):
    open('k2/c_%s.c' % t, 'w', newline='\n').write(s.replace(K, '} else if (!strnicmp(argv[i], "-keys", 5) && ({ __asm__ goto ("" :::: %s); 1; })) {' % t, 1)); n += 1
    open('k2/b_%s.c' % t, 'w', newline='\n').write(s.replace(K, K + ' __asm__ goto ("" :::: %s);' % t, 1)); n += 1
    open('k2/e_%s.c' % t, 'w', newline='\n').write(s.replace(K + '\n\t\t\tmode = 3;\n\t\t\targ = dummy;', K + '\n\t\t\tmode = 3;\n\t\t\targ = dummy; __asm__ goto ("" :::: %s);' % t, 1)); n += 1
print(n)
