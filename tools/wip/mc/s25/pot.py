"""pot.py IN.jsonl OUT.jsonl [N] : 'potential' of measured variants: re-measure each edit set into a
slot, then exhaustive hsim over f of 126 125 127 117 130 (0..2) x RX chains (126->125, 117->130)
on its real history.  Objective: true inversions, case blocks taken over by x1 not counted."""
import sys, os, json, itertools
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, ev, voc
BL = [126, 125, 127, 117, 130]


def tinv(o):
    inv, miss, oo = ev.score_order([str(b) for b in o])
    return inv + 5 * len([b for b in miss if b not in ev.CASES])


def potential(tag):
    sd = os.path.join(R, 'build', 'v', 'mc25', 'slot_' + tag)
    Rr, keys = hsim.load(sd)
    f0, P0 = hsim.measured(keys)
    best = (999,)
    for rx in [(), ('126:125',), ('117:130',), ('126:125', '117:130')]:
        hsim.RXEV.clear()
        for it in rx:
            s, t = map(int, it.split(':')); hsim.RXEV.setdefault(s, []).append(t)
        for fv in itertools.product(range(3), repeat=len(BL)):
            f = dict(f0); P = dict(P0)
            for b, a in zip(BL, fv): f[b] = a
            if '126:125' in rx: P[125] = 1 if f[126] >= 1 else 0
            if '117:130' in rx: P[130] = 1 if f[117] >= 1 else 0
            o = hsim.sim(Rr, f, P)
            x = tinv(o)
            if x < best[0]: best = (x, rx, fv, ' '.join(map(str, o[12:])))
    hsim.RXEV.clear()
    return best


RANGE = {112: range(0, 6), 103: range(0, 6), 115: range(1, 6), 126: range(0, 3), 125: range(0, 3), 127: range(0, 2),
         117: range(0, 2), 130: range(0, 2)}


def potential2(tag):
    """coordinate descent over f of RANGE's blocks (3 passes) from the measured f, per RX option."""
    sd = os.path.join(R, 'build', 'v', 'mc25', 'slot_' + tag)
    Rr, keys = hsim.load(sd)
    f0, P0 = hsim.measured(keys)
    best = (999,)
    for rx in [(), ('126:125',), ('117:130',), ('126:125', '117:130')]:
        hsim.RXEV.clear()
        for it in rx:
            s, t = map(int, it.split(':')); hsim.RXEV.setdefault(s, []).append(t)

        def val(f):
            P = dict(P0)
            if '126:125' in rx: P[125] = 1 if f[126] >= 1 else 0
            if '117:130' in rx: P[130] = 1 if f[117] >= 1 else 0
            o = hsim.sim(Rr, f, P)
            return tinv(o) + 0.1 * sum(abs(f[b] - f0[b]) for b in RANGE if b in f0), o
        f = dict(f0); cur, o = val(f)
        for _ in range(3):
            for b in RANGE:
                if b not in f: continue
                for v in RANGE[b]:
                    g = dict(f); g[b] = v
                    x, oo = val(g)
                    if x < cur: cur, f, o = x, g, oo
        if cur < best[0]:
            best = (cur, rx, {b: f[b] for b in RANGE if b in f and f[b] != f0[b]}, ' '.join(map(str, o[12:])))
    hsim.RXEV.clear()
    return best


if __name__ == '__main__':
    L = [json.loads(l) for l in open(sys.argv[1])]
    L = [x for x in L if not x['miss']]
    L.sort(key=lambda x: x['score'])
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    tag = os.environ.get('TAG', 'pot')
    with open(sys.argv[2], 'a') as f:
        for x in L[:N]:
            r = ev.ev(voc.make(x['e']), tag, fncmp=False)
            if r is None: continue
            b = potential(tag)
            f.write(json.dumps({'e': x['e'], 'score': r['score'], 'pot': b[0], 'rx': b[1], 'fv': b[2], 'o': b[3]}) + '\n')
            f.flush()
            print(r['score'], b, flush=True)
