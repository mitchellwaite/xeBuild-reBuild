"""flsub2.py: dead-test subsets at the natural tail (flash else, sec after, seclen nest),
flen asm/nest/plain.  Writes the best matching source's name list to sub2.txt."""
import itertools, sys
import fllib as L, flpi as P

V = {}
names = P.ALLDEAD
flens = sys.argv[1].split(',') if len(sys.argv) > 1 else ['nest', 'asm']
L.FLAGS[:] = ['-O3']
for fl in flens:
    for r in range(len(names) + 1):
        for rm in itertools.combinations(names, r):
            V[fl + '__' + '+'.join(rm)] = P.gen('else', 'after', 'nest', fl, 'else', dead=rm)
print(len(V))
rs = L.sweep(V, prefix='sb2', show=30)
with open(L.BD + '/sub2.txt', 'w', newline='\n') as f:
    for n, (sc, st, fd, sd) in rs:
        f.write('%s %s %s %s\n' % (sc, n, fd, sd))
