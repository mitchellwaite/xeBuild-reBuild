# wp.py: best's event stream + prof (matching build) keys mapped to best's blocks
import sys, itertools
from wi import *
M = {133:142,109:113,111:116,112:119,115:122,110:115,122:129,123:131,124:134,132:141,118:126,136:147,49:49,117:125,114:121,104:108,55:55,129:139,128:138,61:62,33:33,29:29,67:69,131:140,119:127,134:145,35:35,42:42,53:53,77:79,79:81,73:75,81:83,86:88,140:154,95:97,141:155,96:98,91:93,93:95}
def profkeys():
    pre, g, first = r4sim.load('pf/mc.bbro'); ks = {}
    for e in pre:
        if e[0] == 'push': ks[e[1]] = e[2]
        if e[0] == 'ins' and e[1] != 'this': ks[e[2]] = e[3]
        if e[0] == 'chg': ks[e[1]] = e[2]
    gk = {}
    for b in first:
        for e in g[b]:
            if e[0] == 'ins': gk[e[2]] = e[3]
    return ks, gk
ks, gk = profkeys()
ov = {}
for p, b in M.items():
    if p in ks: ov[b] = ks[p]
    if p in gk: ov[b] = gk[p]
pre, g, first = r4sim.load('dmp_best/mc.bbro')
p2 = push141(pre, ov[141])
o = srch.sim(p2, g, ov); print('all', srch.dist(o), ' '.join(map(str, o)))
print(sorted(ov.items()))
# minimal subsets: greedy removal
cur = dict(ov)
for b in sorted(ov):
    t = dict(cur); del t[b]
    if b == 141: continue
    if srch.dist(srch.sim(p2, g, t)) == 0: cur = t
print('minimal', sorted(cur.items()), srch.dist(srch.sim(p2, g, cur)))
