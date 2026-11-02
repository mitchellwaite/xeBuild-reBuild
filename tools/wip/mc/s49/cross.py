"""cross.py SLOT_A SLOT_B: sim history of A with keys of B (and both own), plus single-key transplants."""
import sys, os
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R0, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.join(R0, r'tools\wip'))
import hsim
Ra, ka = hsim.load(sys.argv[1]); fa, Pa = hsim.measured(ka)
Rb, kb = hsim.load(sys.argv[2]); fb, Pb = hsim.measured(kb)
def run(R, f, P, lab):
    o = hsim.sim(R, f, P); print(lab, hsim.inv(o), ' '.join(map(str, o)))
run(Ra, fa, Pa, 'A/A'); run(Ra, fb, Pb, 'A/B'); run(Rb, fb, Pb, 'B/B'); run(Rb, fa, Pa, 'B/A')
# minimal transplant of B keys into A
diffk = [b for b in set(fa) | set(fb) if (fa.get(b), Pa.get(b)) != (fb.get(b), Pb.get(b)) and b < 1000]
print('diff keys', sorted(diffk))
for b in sorted(diffk):
    f = dict(fa); P = dict(Pa); f[b] = fb.get(b, 0); P[b] = Pb.get(b, 0)
    print(' +%d' % b, hsim.inv(hsim.sim(Ra, f, P)))
import itertools
best = []
for n in (1, 2, 3):
    for S in itertools.combinations(sorted(diffk), n):
        f = dict(fa); P = dict(Pa)
        for b in S: f[b] = fb.get(b, 0); P[b] = Pb.get(b, 0)
        o = hsim.sim(Ra, f, P); best.append((hsim.inv(o), S, o))
best.sort(key=lambda x: x[0])
for i, S, o in best[:8]: print(i, S, ' '.join(map(str, o)))
