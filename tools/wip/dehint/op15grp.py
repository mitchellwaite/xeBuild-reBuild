"""Attempt 15: joint key changes of a group of round-4 entries (every combination within
+-W of each entry's key) through p1/sim3's replay; reports combinations that give REFTAG's
order.  python tools/wip/dehint/op15grp.py REFTAG TAG W b1,b2,.."""
import itertools, os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'aio', 'p1'))
sys.path.insert(0, os.path.join(H, '..'))
import sim3
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')
ref, tag, W, bs = sys.argv[1], sys.argv[2], int(sys.argv[3]), [int(x) for x in sys.argv[4].split(',')]
_, _, f3r, _, f4r = sim3.load(os.path.join(R, ref, 'aio.bbro'))
pre, g3, f3, g4, f4 = sim3.load(os.path.join(R, tag, 'aio.bbro'))
keys = {}
for e in pre + [e for gs in (g3, g4) for v in gs.values() for e in v]:
    if e[0] == 'ins':
        keys.setdefault(e[2], e[3])
    elif e[0] == 'push':
        keys.setdefault(e[1], e[2])
n = 0
for ds in itertools.product(range(-W, W + 1), repeat=len(bs)):
    ov = {b: keys[b] + d for b, d in zip(bs, ds) if d}
    if not ov or max(ov.values()) > 0:
        continue
    o3, o4 = sim3.sim(pre, g3, g4, ov)
    s3, s4 = set(o3), set(o4)
    if [x for x in f3r if x in s3] == o3 and [x for x in f4r if x in s4] == o4:
        print('hit', ov); n += 1
print(n, 'hits;', 'keys', {b: keys[b] for b in bs})
