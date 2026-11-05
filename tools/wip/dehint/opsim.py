"""opsim.py REFTAG TAG shift_from shift [b=key ...] [+parent:pos:key ...]
Replays TAG's rounds 3+4 (p1/sim3.py) with key overrides b=key and extra dummy heap entries
(+parent:pos:key inserts 'Possible start of this round' with that key into round 4 after event
pos of parent's group), maps ids onto REFTAG's numbering and compares the extraction order with
REFTAG's real one (REFTAG-only heads, e.g. zero-byte dummies, are dropped from the comparison)."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'aio', 'p1'))
sys.path.insert(0, os.path.join(H, '..'))
import sim3
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')


def run(ref, tag, sf, sh, ov, dums=(), verbose=True):
    _, _, f3r, _, f4r = sim3.load(os.path.join(R, ref, 'aio.bbro'))
    pre, g3, f3, g4, f4 = sim3.load(os.path.join(R, tag, 'aio.bbro'))
    G4 = {b: list(v) for b, v in g4.items()}
    for n, (p, pos, k) in enumerate(dums):
        G4.setdefault(p, []).insert(min(pos, len(G4[p])), ('ins', 'this', 9000 + n, k))
    o3, o4 = sim3.sim(pre, g3, G4, ov)
    mp = lambda x: x + sh if sf <= x < 9000 else x
    m3 = [mp(x) for x in o3]
    m4 = [mp(x) for x in o4 if x < 9000]
    s3 = set(m3); s4 = set(m4)
    r3 = [x for x in f3r if x in s3]; r4 = [x for x in f4r if x in s4]
    ok3 = r3 == m3; ok4 = r4 == m4
    if verbose:
        print('r3', 'same' if ok3 else 'DIFF', 'r4', 'same' if ok4 else 'DIFF')
        for nm, a, b in (('r3', r3, m3), ('r4', r4, m4)):
            if a != b:
                i = next(i for i in range(min(len(a), len(b))) if a[i] != b[i])
                print(nm, 'first diff at', i, 'ref', a[i:i + 12], 'sim', b[i:i + 12])
    return ok3 and ok4


if __name__ == '__main__':
    a = sys.argv[1:]
    ref, tag, sf, sh = a[0], a[1], int(a[2]), int(a[3])
    ov = {}; dums = []
    for x in a[4:]:
        if x.startswith('+'):
            p, pos, k = x[1:].split(':'); dums.append((int(p), int(pos), int(k)))
        else:
            b, k = x.split('='); ov[int(b)] = int(k)
    run(ref, tag, sf, sh, ov, dums)
