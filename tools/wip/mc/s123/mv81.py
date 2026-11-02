from rm import *
print('g55 ours:', g[55]); 
pp, pg, pf_ = r4sim.load('pf/mc.bbro'); print('g55 prof:', [tuple(PM.get(x, x) if isinstance(x, int) and abs(x) > 1 else x for x in e) for e in pg[55]])
def pdist(o):
    common = [b for b in prof if b in set(o)]; oc = [b for b in o if b in set(common)]; return lcsd(oc, common)
e81 = [e for e in g[55] if e[0] == 'ins' and e[2] == 81][0]
rest = [e for e in g[55] if e is not e81]
for pos in range(len(rest) + 1):
    g2 = dict(g); g2[55] = rest[:pos] + [e81] + rest[pos:]
    o = srch.sim(pre, g2); print(pos, 'pdist', pdist(o), ' '.join(map(str, o[o.index(147):o.index(75)+1])))
print('--- combos')
import itertools
for pos in (3, 9):
  for ov in ({}, {147: -1}, {131: -1}, {147: -1, 131: -1}, {145: -1}, {146: -2}, {55: -3}, {145: -1, 146: -2, 55: -3}, {145: -1, 146: -2, 55: -3, 147: -1}, {108: -5, 129: -4, 122: -3}):
    g2 = dict(g); g2[55] = rest[:pos] + [e81] + rest[pos:]
    o = srch.sim(pre, g2, ov); print(pos, ov, 'pdist', pdist(o), ' '.join(map(str, o[o.index(49):])))
