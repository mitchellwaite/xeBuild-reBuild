"""wi6.py SLOT: add a dummy key-0 block (9999) push/ins at every group position in rounds 3-4; report tail order."""
import sys, copy
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import hsim
R, keys = hsim.load(sys.argv[1])
hsim.mcsim2.pos.setdefault(9999, 999)
T = [35, 42, 53, 77, 79]
for ri in (2, 3):
    for gb in R[ri]['g']:
        for i in range(len(R[ri]['g'][gb]) + 1):
            R2 = copy.deepcopy(R); l = R2[ri]['g'][gb]
            e = ('push', 9999, 0) if ri == 2 else ('ins', 'this', 9999, 0)
            R2[ri]['g'][gb] = l[:i] + [e] + l[i:]
            o = hsim.sim(R2, {}, {})
            print(ri + 1, gb, i, [x for x in o if x in T], hsim.inv([x for x in o if x != 9999]))
