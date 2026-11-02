# tie.py DUMP : 139 group insert permutations/keys for 146/144/143 -> order after 108
import sys, itertools; sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
pre, g, first = r4sim.load(sys.argv[1])
L0 = [e for e in g[139] if e[0] == 'ins']; rest = [e for e in g[139] if e[0] != 'ins']
for perm in itertools.permutations(L0):
  for k3 in (-3, -2, -1):
    for k4 in (-3, -2, -1):
      gg = dict(g); P = [(e[0], e[1], e[2], {143: k3, 144: k4}.get(e[2], e[3])) for e in perm]
      gg[139] = rest + P
      o = r4sim.sim(pre, gg, {}); j = o.index(108)
      print([e[2] for e in perm], k3, k4, o[j:j+16])
