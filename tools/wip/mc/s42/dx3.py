import sys, os, copy, time
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, '.')
import hsim, pot
R, k = hsim.load(os.path.join(R0, 'build', 'v', 'mc42', 'slot_' + sys.argv[1])); f, P = hsim.measured(k)
t = time.time(); hsim.sim(R, f, P); print('dt', time.time() - t)
DS = [None]
for ri in (1, 2):
    for g in R[ri]['g']:
        for K in (-7, -4, -2, -1, 0, -1000404):
            for n in (1, 2): DS.append((ri, g, K, n))
FD = [None] + [(b, d) for b in f for d in (-2, -1, 1, 2) if f[b] + d >= 0]
res = []
for ds in DS:
    R2 = R
    if ds:
        ri, g, K, n = ds; R2 = copy.deepcopy(R)
        R2[ri]['g'][g] = R2[ri]['g'][g] + [('push', 9990 + j, K) for j in range(n)]
    for fd in FD:
        g2 = dict(f)
        if fd: g2[fd[0]] += fd[1]
        try: o = hsim.sim(R2, g2, P)
        except Exception: continue
        res.append((pot.tinv(o), ds, fd, ' '.join(map(str, o))[:150]))
res.sort(key=lambda z: z[0])
for r in res[:15]: print(r)
