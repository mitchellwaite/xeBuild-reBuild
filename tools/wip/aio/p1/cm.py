"""cm.py TAG: multiset of instructions ours vs ref in applyIniOptions; prints +/- with counts."""
import sys, collections, re, ev
o = ev.os.path.join(ev.ROOT, 'build/v/aio_p1', sys.argv[1], 'o.o')
a = ev.funcs(ev.REFO)['_applyIniOptions']; b = ev.funcs(o)['_applyIniOptions']
f = lambda l: collections.Counter(x for x in l if not ev.NOPS.match(x.split(' @')[0]))
A, B = f(a), f(b)
print('ref', sum(A.values()), 'ours', sum(B.values()))
for k, v in sorted((A - B).items()): print('-', v, k)
for k, v in sorted((B - A).items()): print('+', v, k)
