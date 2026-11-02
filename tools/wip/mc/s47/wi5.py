"""wi5.py SLOT B: move the push/ins of block B (key 0) to every group position in rounds 3-4; report tail order."""
import sys, copy
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import hsim
R, keys = hsim.load(sys.argv[1]); B = int(sys.argv[2])
T = [35, 42, 53, 77, 79]
def strip(R):
    for r in R:
        r['pre'] = [e for e in r['pre'] if not (e[0] in ('push', 'ins') and (e[1] == B if e[0] == 'push' else e[2] == B))]
        for g in r['g']:
            r['g'][g] = [e for e in r['g'][g] if not (e[0] in ('push', 'ins') and (e[1] == B if e[0] == 'push' else e[2] == B))]
o = hsim.sim(R, {}, {}); print('base', [x for x in o if x in T], hsim.inv(o))
for ri in (2, 3):
    for gb in R[ri]['g']:
        for i in range(len(R[ri]['g'][gb]) + 1):
            R2 = copy.deepcopy(R); strip(R2); l = R2[ri]['g'][gb]
            e = ('push', B, 0) if ri == 2 else ('ins', 'this', B, 0)
            R2[ri]['g'][gb] = l[:i] + [e] + l[i:]
            try: o = hsim.sim(R2, {}, {})
            except Exception as x: continue
            print(ri + 1, gb, i, [x for x in o if x in T], hsim.inv(o))
