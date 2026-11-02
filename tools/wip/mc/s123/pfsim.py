# pfsim.py: (a) remove all extras at once; (b) profiled event stream with best18's keys (mapped)
import sys
from rm import *
r = evals(EXTRA); print('all extras removed: want-dist', r[0], 'prof-dist', r[1]); print(' ', strip(r[2], set(EXTRA)))
inv = {v: k for k, v in PM.items()}
pp, pg, pfirst = r4sim.load('pf/mc.bbro')
def keys(pre, g):
    ks = {}
    for e in pre + [x for b in g for x in g[b]]:
        if e[0] == 'push': ks[e[1]] = e[2]
        if e[0] == 'ins': ks[e[2]] = e[3]
        if e[0] == 'chg': ks[e[1]] = e[2]
    return ks
ok = keys(pre, g)
ov = {inv[b]: k for b, k in ok.items() if b in inv}
o = srch.sim(pp, pg, ov)
om = [PM.get(b, -b) for b in o]
print('prof stream, best18 keys ->', ' '.join(map(str, om)))
print('prof stream, prof keys   ->', ' '.join(str(PM.get(b, -b)) for b in srch.sim(pp, pg)))
wx = [b for b in want if b in set(om)]; omx = [b for b in om if b in set(wx)]
print('want-dist (common blocks)', lcsd(omx, wx))
for a, b in ((152, 79), (75, 79), (108, 129), (145, 55), (146, 55)):
    if a in om and b in om: print(' %d before %d:' % (a, b), om.index(a) < om.index(b), '| ours base:', base.index(a) < base.index(b) if a in base and b in base else '-', '| want:', want.index(a) < want.index(b) if a in want and b in want else '-')
