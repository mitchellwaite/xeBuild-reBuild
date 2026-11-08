#!/usr/bin/env python3
"""Attempt 27: attempt 25's joint dz1 x dz2 key replay (build/op/a25/joint.py) with
op27map.py's map (drop list, no id collisions) instead of the hand map files.

python tools/wip/dehint/op27joint.py REFTAG TAG DZ1,DZ2 [-k1 lo,hi] [-k2 lo,hi] [-keep]
  the two dummies' keys are overridden over the grid; by default the dummies are left out
  of both orders (as joint.py: TAG's DZ ids and REFTAG's 261, 262); -keep compares them too
  (the map must pair them: op27map's gap pairs do)"""
import collections, os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
from op27ctl import Replay

a = sys.argv[1:]
opt = lambda k, d: [int(x) for x in a[a.index(k) + 1].split(',')] if k in a else d
DZ = [int(x) for x in a[2].split(',')]
K1, K2 = opt('-k1', [-120, -15]), opt('-k2', [-40, 0])
rp = Replay(a[0], a[1])
keep = '-keep' in a
ig, rig = ((), ()) if keep else (DZ, (261, 262))
print('map', sorted((k, v) for k, v in rp.map.items() if k != v)[:6], '.. drop', sorted(rp.drop))
print('as is', *rp.check(ignore=ig, refignore=rig, why=True))
by = collections.defaultdict(list)
best = None
for k1 in range(K1[0], K1[1] + 1):
    for k2 in range(K2[0], K2[1] + 1):
        ok, why = rp.check(ov={DZ[0]: k1, DZ[1]: k2}, ignore=ig, refignore=rig, why=True)
        if ok:
            by[k2].append(k1)
for k2 in sorted(by):
    print('dz2', k2, 'dz1', min(by[k2]), max(by[k2]), len(by[k2]))
print(sum(len(v) for v in by.values()), 'hits')
