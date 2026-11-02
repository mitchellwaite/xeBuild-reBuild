import sys, os, copy
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, '.')
import hsim, pot
R, k = hsim.load(os.path.join(R0, 'build', 'v', 'mc39', 'slot_' + sys.argv[1])); f, P = hsim.measured(k)
print('base', pot.tinv(hsim.sim(R, f, P)))
res = []
for ri in range(len(R)):
    for g in list(R[ri]['g']):
        for K in (-9,-8,-7,-6,-5,-4,-3,-2,-1,0,-60,-1000106,-1000404):
            for n in (1, 2, 3):
                R2 = copy.deepcopy(R)
                for j in range(n): R2[ri]['g'][g] = R2[ri]['g'][g] + [('push', 9990 + j, K)]
                try: o = hsim.sim(R2, f, P)
                except Exception as e: continue
                res.append((pot.tinv(o), ri, g, K, n, ' '.join(map(str, o))[:160]))
# removals of push events
for ri in range(len(R)):
    for g in list(R[ri]['g']):
        evs = R[ri]['g'][g]
        for i, e in enumerate(evs):
            if e[0] in ('push', 'ins'):
                R2 = copy.deepcopy(R); R2[ri]['g'][g] = evs[:i] + evs[i + 1:]
                try: o = hsim.sim(R2, f, P)
                except Exception: continue
                res.append((pot.tinv(o), ri, g, 'del', e, ' '.join(map(str, o))[:160]))
res.sort(key=lambda z: z[0])
for r in res[:25]: print(r)
