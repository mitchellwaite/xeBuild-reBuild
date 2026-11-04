"""fl4a.py: sections moved to static functions called once, all 64 subsets, at a few dead-test states."""
import itertools, sys
import fl4lib as F

SECS = ['files', 'bl', 'cbb', 'raw', 'flash', 'sec']
V = {}
for lab in sys.argv[1:] or ['', 'nb,len,nul,off4']:
    for r in range(0, 7):
        for c in itertools.combinations(SECS, r):
            V['%s|%s' % (lab, '+'.join(c))] = F.gen(F.st(lab), c)
print(len(V))
F.run(V, 'a', show=30)
