import re, sys
src = open('b0.c', newline='').read()
L = src.split('\n')
def w(name, s): open(name + '.c', 'w', newline='').write(s)
orks = dict(re.findall(r'ork(\d+): goto (\w+);', src))
def retarget(s, n, t): return s.replace('ork%s: goto %s;' % (n, orks[n]), 'ork%s: goto %s;' % (n, t), 1)
for X in ['c1','c12','s5','c3','c8','c10','cdef','t4','t5']:
    w('p_' + X, retarget(src, '11', X))
    n = [k for k, v in orks.items() if v == X][0]
    w('m_' + X, retarget(src, n, 'rkE'))
for X in ['c10','c9','c1','c7','cdef']:
    w('f_' + X, src.replace('p1, i1, dtg, ndl, c10, c9, c1, c7, cdef,', 'p1, i1, dtg, ndl, c10, c9, c1, c7, cdef,'.replace(' ' + X + ',', ''), 1))
D = '__asm__ goto ("" :::: dsp);'
cases = {'c1': 'AT(c1) netDumpNand(arg);', 'c3': 'AT(c3)  { JMP(hdd4,s5,hdd5); clientKeys(); }', 'c9': 'AT(c9) { clientWriteBlocks(arg, start); JMP(hdd4,hdd5); }'}
for X, anchor in cases.items():
    i = [j for j, l in enumerate(L) if anchor in l][0]
    k = L[i+1].count(D)
    for d in (-1, 1):
        LL = list(L); LL[i+1] = LL[i+1].replace(D * k, D * (k + d), 1) if k + d >= 0 else LL[i+1]
        w('d_%s%+d' % (X, d), '\n'.join(LL))
