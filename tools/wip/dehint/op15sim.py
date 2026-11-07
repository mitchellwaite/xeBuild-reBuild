"""Attempt 15: wider model search than op13sim.py: which key changes of real heap entries
(any rounds' entries, through p1/sim3.py's replay) make TAG's extraction order equal REFTAG's.

python tools/wip/dehint/op15sim.py REFTAG TAG [-lo L] [-hi H] [-d D] [-2 W] [-only b1,b2]
  singles: every entry, every key in [L, H] (default -200..0)
  -2 W: pairs of entries with keys >= L, each moved by -W..W (default off)
  -only: restrict to these entries
  -map a:b,..: rename TAG's block a to b before comparing (ids that swapped)"""
import itertools, os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'aio', 'p1'))
sys.path.insert(0, os.path.join(H, '..'))
import sim3
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')

a = sys.argv[1:]
ref, tag = a[0], a[1]
opt = lambda k, d: int(a[a.index(k) + 1]) if k in a else d
LO, HI, W = opt('-lo', -200), opt('-hi', 0), opt('-2', 0)
only = set(int(x) for x in a[a.index('-only') + 1].split(',')) if '-only' in a else None
_, _, f3r, _, f4r = sim3.load(os.path.join(R, ref, 'aio.bbro'))
pre, g3, f3, g4, f4 = sim3.load(os.path.join(R, tag, 'aio.bbro'))


MAP = dict(tuple(int(y) for y in x.split(':')) for x in a[a.index('-map') + 1].split(',')) if '-map' in a else {}


def ok(ov):
    o3, o4 = sim3.sim(pre, g3, g4, ov)
    o3 = [MAP.get(x, x) for x in o3]; o4 = [MAP.get(x, x) for x in o4]
    s3 = set(o3); s4 = set(o4)
    return [x for x in f3r if x in s3] == o3 and [x for x in f4r if x in s4] == o4


keys = {}
for e in pre:
    if e[0] == 'ins':
        keys.setdefault(e[2], e[3])
    elif e[0] == 'push':
        keys.setdefault(e[1], e[2])
for gs in (g3, g4):
    for evs in gs.values():
        for e in evs:
            if e[0] == 'ins':
                keys.setdefault(e[2], e[3])
            elif e[0] == 'push':
                keys.setdefault(e[1], e[2])
print('base', ok({}))
cand = sorted(b for b, k in keys.items() if LO <= k <= HI and (only is None or b in only))
hits = 0
for b in cand:
    k = keys[b]
    hs = [nk for nk in range(LO, HI + 1) if nk != k and ok({b: nk})]
    if hs:
        hits += 1
        print('block %d key %d -> %s' % (b, k, hs if len(hs) < 12 else '%d..%d (%d values)' % (hs[0], hs[-1], len(hs))))
print(hits, 'singles over', len(cand), 'entries')
if W:
    n = 0
    for b1, b2 in itertools.combinations(cand, 2):
        k1, k2 = keys[b1], keys[b2]
        for d1 in range(-W, W + 1):
            for d2 in range(-W, W + 1):
                if not d1 or not d2:
                    continue
                ov = {b1: k1 + d1, b2: k2 + d2}
                if max(ov.values()) > 0:
                    continue
                if ok(ov):
                    print('pair', b1, k1, k1 + d1, b2, k2, k2 + d2)
                    n += 1
    print(n, 'pair hits')
