# gf.py BASE.c PREFIX : compensating dead-cp feeds into callee labels of the inlined erase (h0/ef family)
# For each site (case line) x target label x conj count, insert `if (cp(argc+K)&&...) goto L;` after AT(cN).
import sys
base, pre = sys.argv[1], sys.argv[2]
targets = sys.argv[3].split(',') if len(sys.argv) > 3 else ['esucc_i']
src = open(base).read()
sites = ['AT(c2) ', 'AT(c3)  ', 'AT(c7)  ', 'AT(c8) ', 'AT(c9) ', 'AT(c11) ', 'AT(c12) ']
k = 0
for t in targets:
    for si, s in enumerate(sites):
        assert s in src, s
        for nc in (1, 2, 3):
            k += 1
            cond = ' && '.join('__builtin_constant_p(argc+%d)' % (8000 + 100 * k + j) for j in range(nc))
            out = src.replace(s, s + 'if (%s) goto %s; ' % (cond, t), 1)
            n = '%s_%s_%d_%d' % (pre, t.replace('_i', ''), si, nc)
            open('v_%s.c' % n, 'w', newline='\n').write(out)
            print(n)
