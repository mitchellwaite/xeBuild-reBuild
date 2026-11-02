src = open('b0.c', newline='').read()
def ret(s, n, X):
    a = 'ofa%d: goto fkA2;' % n; assert a in s; return s.replace(a, 'ofa%d: goto %s;' % (n, X), 1)
for X in ['c12','c1','c3','t4','t5','c2','c8','c11','c7','c9']:
    open('q_%s.c' % X, 'w', newline='').write(ret(src, 0, X))
s = src
for n in range(3): s = ret(s, n, 'c12')
open('q3_c12.c', 'w', newline='').write(s)
s = src
for n, X in enumerate(['c12','c12','c12','c1','c1','c3','c3','t4','t5','c2','c8']): s = ret(s, n, X)
open('q_lad.c', 'w', newline='').write(s)
