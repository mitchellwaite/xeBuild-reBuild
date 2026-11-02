"""graft.py A B: sim all mixes of rounds (A's rounds with B's rounds substituted) under A keys and B keys."""
import sys, os, itertools
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R0, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.join(R0, r'tools\wip'))
import hsim
Ra, ka = hsim.load(sys.argv[1]); fa, Pa = hsim.measured(ka)
Rb, kb = hsim.load(sys.argv[2]); fb, Pb = hsim.measured(kb)
for mask in itertools.product('AB', repeat=len(Ra)):
    R = [(Ra if m == 'A' else Rb)[i] for i, m in enumerate(mask)]
    for kl, f, P in (('kA', fa, Pa), ('kB', fb, Pb)):
        try: o = hsim.sim(R, f, P); print(''.join(mask), kl, hsim.inv(o), ' '.join(map(str, o)))
        except Exception as e: print(''.join(mask), kl, 'err', e)
