"""python tools/wip/dehint/bdpsweep2.py base:hint[,hint] ... [-r LO-HI]: as bdpsweep.py, on gen_bd540's bases (src, and9, c2,
c6, noi, wt) and with its extra items (etype, cp); prints loadBlFiles loose/strict and the object's (attempt 42)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bdgen'))
import bdlib, bdrun, gen_bd540 as g
from concurrent.futures import ThreadPoolExecutor
a = sys.argv[1:]
lo, hi = 60, 99
if '-r' in a:
    i = a.index('-r'); lo, hi = map(int, a[i + 1].split('-')); del a[i:i + 2]
src = bdlib.read_src()
jobs = []
for spec in a:
    b, _, hs = spec.partition(':')
    t = g.offs(g.BASES[b](src), [h for h in hs.split(',') if h])
    for p in list(range(lo, hi + 1)) + [None]:
        jobs.append((spec, p, t))
def one(j):
    spec, p, t = j
    fl = [] if p is None else ['--param', 'builtin-expect-probability=%d' % p]
    return spec, p, bdrun.score(t, fl)
with ThreadPoolExecutor(4) as ex:
    for spec, p, r in ex.map(one, jobs):
        if 'err' in r: print(spec, p, 'ERR'); continue
        lb = (r['L'].get('_loadBlFiles', 0), r['S'].get('_loadBlFiles', 0))
        print(spec, 'noparam' if p is None else p, 'IDENTICAL' if r['identical'] else 'lbf %d/%d  obj L%d S%d %s' % (lb + (sum(r['L'].values()), sum(r['S'].values()), ','.join(r['notes']))), flush=True)
