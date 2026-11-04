"""fl3o.py <N> <seed> [ADD]: arm sizes around `len=3,off3=2,off4=1,x=2` plus a test at rawpatch's `if (comma == -1 ...` (r2), which fixes tie 1 without an uninitialised read.
Sites r2 and x etc. get re-rolled; a state's arm is k stores or one assignment."""
import random, sys, threading
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import fllib as L, fl3g as G

N, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
G.mark('r2', '\t\t\tif (comma == -1 || comma >= nul) {', '\t\t\t')
G.mark('r6', '\t\t\tp = &buf[pos];\n\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tcomma = memFindChar(p, \',\', size - pos);\n@@r2', '\t\t\t')
G.mark('r3', '\t\t\tif (comma <= 1023) {', '\t\t\t')
G.mark('r4', '\t\t\tif (pos >= end)\n\t\t\t\ti = 16;', '\t\t\t')
SPELL = ['len < -1', 'len < 0']
ASG = ['pos = size', 'i = 0', 'len = 0', 'pos = 0', 'i = 16', 'pos = end']
V, meta = {}, {}
while len(V) < N:
    keep = {}
    for n, base, lo, hi in (('len', 3, 1, 6), ('off3', 2, 1, 8), ('off4', 1, 1, 6), ('x', 2, 1, 8), ('off5', 0, 1, 6), ('nul', 0, 1, 3), ('i', 0, 1, 3)):
        if base == 0:
            if rng.random() < 0.15:
                keep[n] = rng.randint(lo, hi)
        elif rng.random() < 0.85:
            keep[n] = base if rng.random() < 0.5 else rng.randint(lo, hi)
    st = G.st(','.join('%s=%d' % kv for kv in keep.items())) if keep else {}
    a = rng.choice(ASG + [1, 2, 3])
    where = rng.choice(['r2', 'r2', 'r2', 'r6', 'r3', 'r4'])
    st[where] = (rng.choice(SPELL), a)
    lab = ','.join('%s=%d' % kv for kv in sorted(keep.items())) + '+%s:%s:%s' % (where, st[where][0], a)
    V[lab] = G.gen(st)
    meta[lab] = len(keep) + 1
loc = threading.local()
cnt = [0]
lock = threading.Lock()


def one(kv):
    if not hasattr(loc, 'id'):
        with lock:
            cnt[0] += 1
            loc.id = cnt[0]
    n, s = kv
    o = L.compile(s, None, 'o%d_%d' % (seed, loc.id))
    if o is None:
        return 10**7, '', n
    return L.score(o)[0], G.vec(o), n


with ThreadPoolExecutor(4) as ex:
    rs = sorted(ex.map(one, V.items()), key=lambda r: (r[0], meta[r[2]]))
with open(L.BD + '/a3/o3.txt', 'a', newline='\n') as f:
    for r in rs:
        f.write('%s\t%s\t%s\t%d\n' % (r + (meta[r[2]],)))
print(Counter((r[0], r[1]) for r in rs if r[0] < 30).most_common(10))
for r in rs[:15]:
    print(r, meta[r[2]])
print('MATCH', [(meta[r[2]], r[2]) for r in rs if r[0] == 0][:20])
