# gen5.py: lower the -keys arm frequency (bb96) below round-3 exec_th via dead __builtin_constant_p conjuncts
import os
s = open('b18.c').read()
K = '} else if (!strnicmp(argv[i], "-keys", 5)) {'
assert K in s
def cpn(n, base): return ' && '.join('__builtin_constant_p(i + %d)' % (base + j) for j in range(n))
def cpc(n, base): return ' && '.join('(char *)__builtin_constant_p(i + %d) == (char *)1' % (base + j) for j in range(n))
V = {}
for n in (1, 2, 3):
    V['and%d' % n] = '} else if (!strnicmp(argv[i], "-keys", 5) && !(%s)) {' % cpn(n, 8800)
    V['andc%d' % n] = '} else if (!strnicmp(argv[i], "-keys", 5) && !(%s)) {' % cpc(n, 8800)
    V['pre%d' % n] = '} else if (!(%s) && !strnicmp(argv[i], "-keys", 5)) {' % cpn(n, 8800)
    for t in ('k67l', 'k55l', 'cdef', 'u2', 'r3x', 'wb3', 'k61l'):
        V['g%d_%s' % (n, t)] = '} else if (!strnicmp(argv[i], "-keys", 5) && ({ if (%s) goto %s; 1; })) {' % (cpn(n, 8800), t)
        V['b%d_%s' % (n, t)] = '} else if (!strnicmp(argv[i], "-keys", 5)) { if (%s) goto %s;' % (cpn(n, 8800), t)
for k, v in V.items(): open('k/%s.c' % k, 'w', newline='\n').write(s.replace(K, v, 1))
print(len(V))
