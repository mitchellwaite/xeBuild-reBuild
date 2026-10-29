"""Do small key changes in rounds 2-3 (hot-block frequencies) move mode_client's last-round order?
python tools/wip/mc/mcearly.py <mode_client-only bbro dump> [maxdelta]
Replays round 1 exactly and rounds 2-4 event-driven (tools/wip/fibwhatif.sim, rnd_from=2) with one
block's key changed; prints every change that lowers the inversions against mcsim2.WANT."""
import os, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'wip'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'wip', 'mc'))
import fibsim, fibwhatif, mcsim2

ev = fibsim.parse(sys.argv[1])
R = fibwhatif.groups(ev)
maxd = int(sys.argv[2]) if len(sys.argv) > 2 else 3
npre = sum(len(r['order']) for r in R[:3])
base = fibwhatif.sim(R, {}, rnd_from=2)
real = [e[1] for e in ev if e[0] == 'get']
print('sim(rnd_from=2)==real', base == real)
bpre, binv, _ = mcsim2.score(base, npre)
print('base pre=%d inv=%d' % (bpre, binv))
# candidate blocks: keys in (-100, 0] inserted/pushed in rounds 1-3
keyed = collections.OrderedDict()
for ri, r in enumerate(R[:3], 1):
    for e in r['pre'] + [x for g in r['g'].values() for x in g]:
        if e[0] == 'ins' and -100 < e[3] <= 0:
            keyed[e[2]] = e[3]
        if e[0] == 'push' and -100 < e[2] <= 0:
            keyed[e[1]] = e[2]
print('candidates', dict(keyed))
res = []
for b, k in keyed.items():
    for d in range(-maxd, maxd + 1):
        if d == 0 or k + d > 0:
            continue
        try:
            o = fibwhatif.sim(R, {b: k + d}, rnd_from=2)
        except Exception as ex:
            continue
        pre, inv, oo = mcsim2.score(o, npre)
        res.append((inv, -pre, b, k, k + d, oo))
res.sort()
for inv, mpre, b, k, nk, oo in res[:25]:
    print('inv=%2d pre=%2d  bb %d: %d -> %d   %s' % (inv, -mpre, b, k, nk, ' '.join(map(str, oo[12:22]))))
