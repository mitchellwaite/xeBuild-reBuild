# gp.py BASE.c PREFIX L1 L2 : pairs of dead-cp feeds (L1 from site a, L2 from site b), 1 conjunct each
import sys
base, pre, l1, l2 = sys.argv[1:5]
src = open(base).read()
sites = ['AT(c1) ', 'AT(c2) ', 'AT(c3)  ', 'AT(c7)  ', 'AT(c8) ', 'AT(c9) ', 'AT(c11) ', 'AT(c12) ']
for a, sa in enumerate(sites):
    for b, sb in enumerate(sites):
        out = src.replace(sa, sa + 'if (__builtin_constant_p(argc+9100)) goto %s; ' % l1, 1)
        out = out.replace(sb, sb + 'if (__builtin_constant_p(argc+9200)) goto %s; ' % l2, 1)
        n = '%s_%d%d' % (pre, a, b)
        open('v_%s.c' % n, 'w', newline='\n').write(out)
        print(n)
