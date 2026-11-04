"""fl4b.py: `files` helper plus every subset of the old dead tests at their arms, and arms 1-3 for subsets of size <= 2."""
import itertools, sys
import fl4lib as F
V = {}
for r in range(0, 8):
    for c in itertools.combinations(F.SITES, r):
        lab = ','.join(c)
        V[lab] = F.gen(F.st(lab), ('files',))
for r in (1, 2):
    for c in itertools.combinations(F.SITES, r):
        for ks in itertools.product((1, 2, 3), repeat=r):
            lab = ','.join('%s=%d' % x for x in zip(c, ks))
            V[lab] = F.gen(F.st(lab), ('files',))
print(len(V))
F.run(V, 'b', show=30)
