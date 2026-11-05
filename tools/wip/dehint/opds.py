"""opds.py REFTAG TAG sf sh [b=key ...]: search one round-4 dummy heap entry (group, position, key)
on top of the overrides that makes TAG's replayed r3/r4 extraction equal REFTAG's (opsim.run)."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opsim, sim3

a = sys.argv[1:]
ref, tag, sf, sh = a[0], a[1], int(a[2]), int(a[3])
ov = dict((int(x.split('=')[0]), int(x.split('=')[1])) for x in a[4:])
_, _, _, g4, f4 = sim3.load(os.path.join(opsim.R, tag, 'aio.bbro'))
keys = list(range(1, 160)) + [k * 100 + k for k in range(1, 60)]
t = time.time()
hits = []
for g in f4:
    n = len(g4.get(g, []))
    for pos in sorted({0, n // 2, n}):
        for k in keys:
            if opsim.run(ref, tag, sf, sh, ov, [(g, pos, -k if k < 1000 else -(1000000 + k))], verbose=False):
                hits.append((g, pos, k))
    print(g, len(hits), '%.0fs' % (time.time() - t), flush=True, file=sys.stderr)
for h in hits:
    print(h)
