"""rel.py TAG: relocate insertion events of one block to another group (hsim)."""
import sys, os, copy
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, '.')
import hsim, pot
R, k = hsim.load(os.path.join(R0, 'build', 'v', 'mc38', 'slot_' + sys.argv[1])); f, P = hsim.measured(k)
def strip(R, b):
    R2 = copy.deepcopy(R); ks = []
    for ri in range(len(R2)):
        for g, evs in R2[ri]['g'].items():
            n = []
            for e in evs:
                if e[0] == 'ins' and e[2] == b: ks.append(e[3]); continue
                if e[0] == 'push' and e[1] == b: continue
                if e[0] == 'chg' and e[1] == b: ks.append(e[2]); continue
                n.append(e)
            R2[ri]['g'][g] = n
    return R2, ks
blocks = set()
for r in R:
    for g, evs in r['g'].items():
        for e in evs:
            if e[0] == 'ins': blocks.add(e[2])
res = []
for b in sorted(blocks):
    if b > 990 and b not in (1118, 1116): pass
    R2, ks = strip(R, b)
    for ri in range(len(R2)):
        for g in list(R2[ri]['g']):
            for K in set(ks):
                for where in ('next', 'this'):
                    R3 = copy.deepcopy(R2); R3[ri]['g'][g] = R3[ri]['g'][g] + [('ins', where, b, K)]
                    try: o = hsim.sim(R3, f, P)
                    except Exception: continue
                    res.append((pot.tinv(o), b, ri, g, K, where, ' '.join(map(str, o))[:150]))
res.sort(key=lambda z: z[0])
for r in res[:30]: print(r)
