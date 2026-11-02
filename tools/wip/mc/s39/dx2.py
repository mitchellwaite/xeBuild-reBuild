import sys, os, copy
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, '.')
import hsim, pot
R, k = hsim.load(os.path.join(R0, 'build', 'v', 'mc39', 'slot_J1')); f, P = hsim.measured(k)
R2 = copy.deepcopy(R)
for ri in range(len(R2)):
    for g, evs in R2[ri]['g'].items():
        R2[ri]['g'][g] = [e for e in evs if not ((e[0]=='push' and e[1]==118) or (e[0]=='ins' and e[2]==118))]
R2[3]['g'][119] = R2[3]['g'][119] + [('ins', 'this', 118, -6), ('chg', 118, -1000106)]
o = hsim.sim(R2, f, P); print(pot.tinv(o), ' '.join(map(str, o)))
R3 = copy.deepcopy(R)
for ri in range(len(R3)):
    for g, evs in R3[ri]['g'].items():
        R3[ri]['g'][g] = [e for e in evs if not ((e[0]=='push' and e[1]==118) or (e[0]=='ins' and e[2]==118))]
o = hsim.sim(R3, f, P); print(pot.tinv(o), ' '.join(map(str, o)))
