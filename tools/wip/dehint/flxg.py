"""flxg.py <vars> [k]: remove k (default 2) of the 8 dead tests (asm kept) and insert one defined-var test
anywhere: a MATCH drops the total by k - 1.  Logs each pair's best to xg.txt as it goes."""
import itertools, sys
import fllib as L, flx as X, flx6 as D

VARS = sys.argv[1].split(',')
k = int(sys.argv[2]) if len(sys.argv) > 2 else 2
out = open(L.BD + '/xg_%d.txt' % k, 'a', newline='\n')
for rm in itertools.combinations(X.ALLDEAD, k):
    base = X.gen(rm, 'asm')
    V, meta = {}, {}
    for p in D.points(base):
        ln = base.count('\n', 0, p) + 1
        for v in VARS:
            n = '%d_%s' % (ln, v)
            V[n] = D.insert(base, p, v)
            meta[n] = base[p:base.index('\n', p)].strip()[:50]
    rs = L.sweep(V, prefix='g', show=0)
    best = [(n, r[0]) for n, r in rs[:3]]
    out.write('%s\t%s\t%s\n' % ('+'.join(rm), best, meta[rs[0][0]]))
    out.flush()
    for n, r in rs:
        if r[0] == 0:
            out.write('MATCH %s %s %s\n' % ('+'.join(rm), n, meta[n]))
            out.flush()
