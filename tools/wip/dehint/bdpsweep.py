"""python tools/wip/dehint/bdpsweep.py hint[,hint] ...: each set of bdhints entries off, scored at builtin-expect-probability 60 to 99 (attempt 32)."""
import sys, os
sys.path.insert(0, 'tools/wip/dehint')
import bdlib, bdhints, bdrun
from concurrent.futures import ThreadPoolExecutor
base = bdlib.read_src()
sets = [s.split(',') for s in sys.argv[1:]]
jobs = [(s, p) for s in sets for p in range(60, 100)]
def one(j):
    s, p = j
    r = bdrun.score(bdhints.off(base, *s), ['--param', 'builtin-expect-probability=%d' % p])
    return s, p, r
with ThreadPoolExecutor(4) as ex:
    for s, p, r in ex.map(one, jobs):
        if 'err' in r: print(s, p, 'ERR'); continue
        print(','.join(s), p, 'IDENTICAL' if r['identical'] else 'S%d L%d' % (sum(r['S'].values()), sum(r['L'].values())))
