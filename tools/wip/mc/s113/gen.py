# gen.py name spec... : variant of b0.c. spec: c11=N (conj count of fail's goto c11, 0 drops it),
#   j:POS:LBL (empty asm goto to LBL inserted at POS)
import re, sys
t = open('b0.c').read()
name = sys.argv[1]
POS = {
 'c6': ('case 6:\n\t\t\t\tbreak;', 'case 6:\n\t\t\t\t%s break;'),
 'c2': ('AT(c2) clientWrite(arg);\n', 'AT(c2) clientWrite(arg);\n\t\t\t\t%s\n'),
 'c10': ('AT(c10) clientEraseBlockI(arg);\n', 'AT(c10) clientEraseBlockI(arg);\n\t\t\t\t%s\n'),
 'c11': ('AT(c11) clientBinPatch(arg, start);\n', 'AT(c11) clientBinPatch(arg, start);\n\t\t\t\t%s\n'),
 'fl': ('unable to connect to xbox server\n");\n', 'unable to connect to xbox server\n");\n\t%s\n'),
 'nd': ('goto u2; \n\treturn 0;', 'goto u2; \n\t%s return 0;'),
 'dt': ('\tdtg: if (E(reboot))', '\tdtg: %s if (E(reboot))'),
 'p1': ('{ AT(p1) clientPatches(arg); }', '{ AT(p1) clientPatches(arg); %s }'),
 'i1': ('{ AT(i1) clientInfo(arg); }', '{ AT(i1) clientInfo(arg); %s }'),
 'c8': ('JMP(p1,cdef); }', 'JMP(p1,cdef); %s }'),
}
for s in sys.argv[2:]:
    if s.startswith('c11='):
        n = int(s[4:])
        m = re.search(r'if \(__builtin_constant_p\(mode \+ 2400\)[^)]*\)( && __builtin_constant_p\(mode \+ \d+\))*\) goto c11;', t)
        assert m
        new = '' if n == 0 else 'if (' + ' && '.join('__builtin_constant_p(mode + %d)' % (2400 + 50000*i) for i in range(n)) + ') goto c11;'
        t = t[:m.start()] + new + t[m.end():]
    elif s.startswith('j:'):
        _, p, l = s.split(':')
        a, b = POS[p]; assert t.count(a) == 1, p
        t = t.replace(a, b % ('__asm__ goto ("" :::: %s);' % l.replace('+', ', ')))
open(name + '.c', 'w', newline='\n').write(t)
