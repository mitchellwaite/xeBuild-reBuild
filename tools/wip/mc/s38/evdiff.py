"""evdiff.py TAG_A TAG_B : diff bbro heap event histories of two slots (round 4) ignoring key values;
prints measured f/P deltas and whether the event sequence is identical (event-neutral)."""
import sys, os
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.join(R, r'tools\wip'))
import hsim
def load(t):
    Rr, keys = hsim.load(os.path.join(R, 'build', 'v', 'mc38', 'slot_' + t))
    f, P = hsim.measured(keys)
    ev = []
    for ri, r in enumerate(Rr, 1):
        ev.append((ri, 'pre', tuple(tuple(x[:3]) if x[0] == 'ins' else tuple(x[:2]) for x in r['pre'])))
        for b, es in r['g'].items():
            ev.append((ri, b, tuple(tuple(x[:3]) if x[0] == 'ins' else tuple(x[:2]) for x in es)))
    return f, P, ev
_C = {}
def diff(a, b):
    if a not in _C: _C[a] = load(a)
    fa, Pa, ea = _C[a]; fb, Pb, eb = load(b)
    df = {k: (fa.get(k), fb.get(k)) for k in set(fa) | set(fb) if fa.get(k) != fb.get(k)}
    dP = {k: (Pa.get(k), Pb.get(k)) for k in set(Pa) | set(Pb) if Pa.get(k) != Pb.get(k)}
    sa, sb = set(ea), set(eb)
    return df, dP, sorted(sa - sb, key=str), sorted(sb - sa, key=str)
if __name__ == '__main__':
    df, dP, onlyA, onlyB = diff(sys.argv[1], sys.argv[2])
    print('df', df); print('dP', dP)
    print('neutral' if not onlyA and not onlyB else 'events differ: %d/%d' % (len(onlyA), len(onlyB)))
    for x in onlyA[:10]: print(' A', x)
    for x in onlyB[:10]: print(' B', x)
