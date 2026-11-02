import sys, itertools
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s111')
from wi import *
pre, g, first = r4sim.load(sys.argv[1])
def K(p, f): return -(1000000 + 100*p + f) if p is not None else -f
print('base', srch.dist(srch.sim(pre, g)), ' '.join(map(str, srch.sim(pre, g))))
res = []
for k141 in [K(3,6),K(3,7),K(2,10),K(3,5),K(2,9)]:
  for k134 in [None, K(3,7), K(3,6), K(3,8), K(2,9)]:
    for k126 in [None, K(3,5), K(2,9), K(2,8), K(3,4)]:
      ov = {}
      if k134: ov[134] = k134
      if k126: ov[126] = k126
      o = srch.sim(push141(pre, k141), g, ov); res.append((srch.dist(o), k141, k134, k126, ' '.join(map(str, o))))
res.sort(key=lambda r: r[0])
for r in res[:8]: print(r)
