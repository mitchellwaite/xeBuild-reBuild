"""Attempt 13: which single (or paired) key changes of real round-4 heap entries make TAG's
replayed extraction order equal REFTAG's (opsim.py / p1 sim3.py).  The point: find a
natural count change that does a dummy's job.

python tools/wip/dehint/op13sim.py REFTAG TAG [sf sh] [-d D] [-2]
  -d D: try keys within D of each entry's own key (default 6); -2: pairs too (slow)"""
import itertools, os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import opsim
import sim3

a = sys.argv[1:]
ref, tag = a[0], a[1]
sf, sh = (int(a[2]), int(a[3])) if len(a) > 3 and not a[2].startswith('-') else (99999, 0)
D = int(a[a.index('-d') + 1]) if '-d' in a else 6
pre, g3, f3, g4, f4 = sim3.load(os.path.join(opsim.R, tag, 'aio.bbro'))
keys = {}
for gs in (g3, g4):
    for b, evs in gs.items():
        for e in evs:
            if e[0] == 'ins':
                keys.setdefault(e[2], e[3])
            elif e[0] == 'push':
                keys.setdefault(e[1], e[2])
for e in pre:
    if e[0] == 'ins':
        keys.setdefault(e[2], e[3])
    elif e[0] == 'push':
        keys.setdefault(e[1], e[2])
hits = []
for b, k in sorted(keys.items()):
    for nk in range(k - D, k + D + 1):
        if nk == k or nk > 0:
            continue
        if opsim.run(ref, tag, sf, sh, {b: nk}, verbose=False):
            hits.append((b, k, nk))
for h in hits:
    print('block %d key %d -> %d' % h)
print(len(hits), 'single hits over', len(keys), 'entries')
if '-2' in a:
    cand = [(b, k) for b, k in keys.items() if k > -400]
    n = 0
    for (b1, k1), (b2, k2) in itertools.combinations(sorted(cand), 2):
        for d1 in (-1, 1):
            for d2 in (-1, 1):
                ov = {b1: k1 + d1, b2: k2 + d2}
                if max(ov.values()) > 0:
                    continue
                if opsim.run(ref, tag, sf, sh, ov, verbose=False):
                    print('pair', b1, k1, k1 + d1, b2, k2, k2 + d2)
                    n += 1
    print(n, 'pair hits')
