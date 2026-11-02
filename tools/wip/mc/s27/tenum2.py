"""tenum2.py TAG : exhaustive hsim over (f, P) of the non-loop tail blocks 126 125 127 117 130 on
slot_TAG's history, with the true inversion count (ev.WANT).  f in 0..2, P in 0..1 (P<=f+1).
Prints the best designs and the measured baseline."""
import sys, os, itertools
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, ev
sd = os.path.join(R, 'build', 'v', 'mc27', 'slot_' + sys.argv[1])
Rr, keys = hsim.load(sd)
f0, P0 = hsim.measured(keys)
BL = [int(x) for x in os.environ.get('BL', '126,125,127,117,130').split(',')]
FV = range(int(os.environ.get('FM', '3')))
PV = range(int(os.environ.get('PM', '2')))


def tinv(o):
    inv, miss, oo = ev.score_order([str(b) for b in o])
    return inv + 5 * len(miss)


o = hsim.sim(Rr, f0, P0)
print('measured', tinv(o), ' '.join(map(str, o[12:])))
res = []
for fv in itertools.product(FV, repeat=len(BL)):
    for pv in itertools.product(PV, repeat=len(BL)):
        f = dict(f0); P = dict(P0)
        for b, a, p in zip(BL, fv, pv): f[b] = a; P[b] = p
        o = hsim.sim(Rr, f, P)
        res.append((tinv(o), fv, pv, ' '.join(map(str, o[12:]))))
res.sort()
for r in res[:12]: print(r)
