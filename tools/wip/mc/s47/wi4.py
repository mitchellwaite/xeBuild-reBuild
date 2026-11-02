"""wi4.py SLOT: add round-3 pushes of 77/79 (key 0) in each round-3 group/position, both orders."""
import sys, copy
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import hsim
R, keys = hsim.load(sys.argv[1])
T = [35, 42, 53, 77, 79]
for ri in (1, 2):
    for gb, evs in R[ri]['g'].items():
        for i in range(len(evs) + 1):
            for a, b in ((77, 79), (79, 77)):
                for ab in ([a, b], [a]):
                    R2 = copy.deepcopy(R); l = R2[ri]['g'][gb]
                    R2[ri]['g'][gb] = l[:i] + [('push', x, 0) for x in ab] + l[i:]
                    try: o = hsim.sim(R2, {}, {})
                    except Exception as x: print('err', ri, gb, x); continue
                    print(ri + 1, gb, i, ab, [x for x in o if x in T], hsim.inv(o))
