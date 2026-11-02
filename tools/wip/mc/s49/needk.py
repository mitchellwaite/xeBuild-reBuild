"""needk.py A B: on B's history, greedily revert B keys to A keys while inv stays <= limit; reports which B keys are essential."""
import sys, os
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R0, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.join(R0, r'tools\wip'))
import hsim
Ra, ka = hsim.load(sys.argv[1]); fa, Pa = hsim.measured(ka)
Rb, kb = hsim.load(sys.argv[2]); fb, Pb = hsim.measured(kb)
f, P = dict(fb), dict(Pb)
lim = hsim.inv(hsim.sim(Rb, f, P))
ks = [b for b in set(fa) | set(fb) if (fa.get(b, 0), Pa.get(b, 0)) != (fb.get(b, 0), Pb.get(b, 0))]
ess = []
for b in sorted(ks):
    g, Q = dict(f), dict(P); g[b] = fa.get(b, 0); Q[b] = Pa.get(b, 0)
    i = hsim.inv(hsim.sim(Rb, g, Q))
    if i <= lim: f, P = g, Q
    else: ess.append((b, (fb.get(b), Pb.get(b)), (fa.get(b), Pa.get(b)), i))
print('base', lim, 'essential B keys:', ess)
o = hsim.sim(Rb, f, P); print(hsim.inv(o), ' '.join(map(str, o)))
