"""s18: priority-key sim (gcc 6.2 bb_to_key) over the vY history (s12 bYr.txt, sp numbering).

New vs fake6: blocks carry a priority P[b] (max EDGE_FREQUENCY from a trace-end pred); once
activated, key = -(1e6 + 100*P + f), else -f.  Design levers modelled:
  * T48: the round-3 trace [48 94] is cut at 48 (f94 <= 9 < exec_th 10, f48 = f94+f49 >= 10):
    94 and 49 are pushed to round 4 and re-keyed with priority P94 = f94, P49 = f49 (49 has the
    single pred 48).  94 then pops first in round 4 (trace [94], no inserts).
  * X2: an asm goto at the end of the rok path block 102 (round-3 trace [102], ends there):
    every target T in TX2 gets P[T] = pX2[T] (edge freq) when 102's trace ends; f[T] >= P[T].
  * X (999, vY) as in fake6 (round-2 mid-trace source, no priority).
python fake7.py ITERS SEED      env: TX2=112,115,103  X1=1  VMAX  P132MAX  SEEDF=json
"""
import random, sys, os, json
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\tools\wip'); sys.path.insert(0, ROOT + r'\tools\wip\mc')
import fibsim, fibwhatif, mcsim2
ev = fibsim.parse(ROOT + r'\tools\wip\mc\s12\bYr.txt'); R = fibwhatif.groups(ev)
CASES = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116, 132]
COLD = [49, 112, 115, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
T48 = os.environ.get('T48', '1') == '1'
X1 = os.environ.get('X1', '1') == '1'
XC = [112, 115, 117, 130, 103] + [c for c in CASES if c not in (110, 113)]
TX1 = frozenset(XC) if X1 else frozenset()
# zero-flow X1 (vY asm goto before the switch's netGetInfo): its targets are inserted (round 2, next heap) in this order
X1ORD = [int(x) for x in os.environ['X1ORD'].split(',') if x] if os.environ.get('X1ORD') is not None else None
TX2 = frozenset(int(x) for x in os.environ.get('TX2', '112,115,103').split(',') if x)
if os.environ.get('X2CASES') == '1': TX2 = TX2 | frozenset(c for c in CASES if c not in (110, 113))
X2ORD = [int(x) for x in os.environ.get('X2ORD', '112,115,103,107,108,109,119,120,121,128,129,116,132,117,130').split(',') if int(x) in TX2]
VMAX = int(os.environ.get('VMAX', '11'))
P132MAX = int(os.environ.get('P132MAX', '3'))
SLACK = int(os.environ.get('SLACK', '0'))
FMAX = int(os.environ.get('FMAX', '9'))
# round-4 trace-end asm-goto sources: RX=126:125,117:130  (src's trace is [src], ends at the asm goto)
RX = {}
for it in os.environ.get('RX', '').split(','):
    if it: s_, t_ = map(int, it.split(':')); RX.setdefault(s_, []).append(t_)


def sim(f, P):
    """f: freq per block (+ f[94]); P: priority per block (cases: P[c]; 49; 94; X2 targets)."""
    heap = fibsim.Heap(); new = None
    loc = {2: (heap, heap.insert(0, 2))}
    act = set()
    vis = set()
    order = []
    def key(b, k):
        if b not in f: return k
        if b in act and P.get(b, 0) > 0: return -(1000000 + 100 * P[b] + f[b])
        return -f[b]
    def ins(h, b):
        if b in loc or b in vis: return
        loc[b] = (h, h.insert(key(b, 0), b))
    def chg(b):
        if b in loc:
            h, n = loc[b]; k = key(b, 0)
            if k != n.key: loc[b] = (h, h.replace_key(n, k))
    def apply(e, ri):
        if e[0] == 'visit':
            vis.add(e[1])
            if e[1] in loc:
                h, n = loc.pop(e[1]); h.delete_node(n)
            if e[1] == 999 and X1:
                for t in TX1: ins(new, t)
        elif e[0] == 'ins':
            h = heap if e[1] == 'this' else new
            if e[2] in loc or e[2] in vis: return
            if e[3] <= -100 and e[2] in f: act.add(e[2])
            loc[e[2]] = (h, h.insert(key(e[2], e[3]), e[2]))
        elif e[0] == 'push':
            if e[1] in loc or e[1] in vis: return
            loc[e[1]] = (new, new.insert(key(e[1], e[2]), e[1]))
        elif e[0] == 'chg':
            if e[1] in loc:
                if e[2] <= -100 and e[1] in f: act.add(e[1])
                h, n = loc[e[1]]; loc[e[1]] = (h, h.replace_key(n, key(e[1], e[2])))
    for ri, r in enumerate(R, 1):
        if new is not None: heap = new
        new = fibsim.Heap()
        for e in r['pre']: apply(e, ri)
        while heap.min is not None:
            z = heap.extract_min(); b = z.data; loc.pop(b, None)
            if b in f and ri < 4 and b not in (48, 102):
                # cold block popped in rounds 2/3 below threshold: pushed to next round
                loc[b] = (new, new.insert(key(b, 0), b)); continue
            order.append((ri, b))
            if ri == 4: vis.add(b)
            evs = r['g'].get(b, [])
            if ri == 3 and b == 48 and T48:
                apply(('visit', 48), ri)
                ins(new, 94); ins(new, 49)
                act.update((94, 49)); chg(94); chg(49)
                continue
            if ri == 3 and b == 102:
                apply(('visit', 102), ri)
                for t in X2ORD: ins(new, t)
                for t in X2ORD:
                    if P.get(t, 0) > 0: act.add(t); chg(t)
                continue
            skip = False
            for e in evs:
                if b in f and e[0] == 'push':  # already handled above
                    continue
                if X1ORD is not None and e == ('visit', 999):
                    apply(e, ri)
                    for t in X1ORD: ins(new, t)
                    skip = True; continue
                if skip:
                    if e[0] == 'ins': continue
                    skip = False
                apply(e, ri)
            if ri == 4 and b in RX:
                for t in RX[b]:
                    if P.get('x%d_%d' % (b, t), 0) > 0 and t in loc:
                        P[t] = max(P.get(t, 0) if t in act else 0, P['x%d_%d' % (b, t)]); act.add(t); chg(t)
    return [b for r, b in order if r == 4 and b in mcsim2.pos]


def inv(o):
    p = mcsim2.pos
    return sum(1 for a in range(len(o)) for b in range(a + 1, len(o)) if p[o[a]] > p[o[b]])


def rmax(x):
    """largest integer freq a real value < x can round to (round half up)"""
    import math
    return int(math.floor(x - 1e-9 + 0.5))


def chain_ok(f):
    x49 = f[49] + 0.5            # real -ip test freq < f49 + .5
    # trace 49 -> 50 needs p(49->55) <= ~50%, likewise 55 -> 56, 61 -> 62
    return f[55] <= rmax(x49 / 2) and f[61] <= rmax(x49 / 4) and f[67] <= rmax(x49 / 8)         and f[61] <= rmax((f[55] + .5) / 2) and f[67] <= rmax((f[61] + .5) / 2)


def ok(f, P):
    for c in CASES:
        if f[c] > FMAX: return False
        if c != 121 and c not in TX1 and c not in TX2 and abs(P[c] - f[c]) > SLACK and c != 132: return False
        if P[c] > f[c]: return False
    if P[132] > P132MAX: return False
    # default case: the RTL range check (105->132) takes about half of the default flow
    if 132 in TX2:
        if not (P[132] <= f[132] <= 3 * P[132]): return False
    elif abs(f[132] - 2 * P[132]) > 1: return False
    if 112 not in TX1 | TX2 and f[112] > f[110] / 2 + .5: return False
    if 115 not in TX1 | TX2 and f[115] > f[113] / 2 + .5: return False
    if 117 not in TX1 | TX2 and f[117] > f[116]: return False
    if 130 not in TX1 | TX2 and f[130] > f[129]: return False
    if f[103] < P.get(103, 0) * (103 in TX2) + int(os.environ.get("U2MIN", "1")): return False
    pass
    x2 = 0
    for t in TX2:
        if t in CASES:
            if t != 132 and f[t] - P[t] > P[t]: return False
        else:
            if P.get(t, 0) > f[t]: return False
            x2 += P.get(t, 0)
    tot = sum(f[c] for c in CASES) + f[132] // 3 + x2
    if tot > int(os.environ.get('FLOWMAX', '112')): return False
    for s_ in RX:
        for t in RX[s_]:
            if P.get('x%d_%d' % (s_, t), 0) > min(f[t] + SLACK, f[s_]): return False
    F48 = int(os.environ.get('F48', '12'))
    if T48 and f[49] + f[94] < F48: return False
    if max(f[b] for b in COLD) > 9: return False
    C10 = f[121]
    if f[127] > C10 or f[126] > C10 / 2 + .5: return False
    if T48:
        if not (f[49] + f[94] >= 10 and f[94] <= 9): return False
        P[49] = max(1, f[49] + P.get('d49', 0)); P[94] = f[94]
    if not chain_ok(f): return False
    if any(f[b] > 5 for b in (35, 42, 53, 77, 79)): return False
    return True


BASE = {112: 5, 115: 5, 127: 1, 126: 2, 125: 2, 49: 5, 55: 3, 61: 2, 67: 1, 103: 5, 117: 1, 130: 1,
        29: 1, 33: 1, 35: 0, 42: 0, 53: 0, 77: 0, 79: 0, 94: 9}
BASE[132] = 6
BP = {}
for c, e in zip(CASES, (7, 7, 7, 6, 6, 6, 6, 6, 6, 4, 4, 4)): BASE[c] = e; BP[c] = e
BP[132] = 5; BP['d49'] = 0
for t in TX2:
    if t not in CASES: BP[t] = 1
for s_ in RX:
    for t in RX[s_]: BP['x%d_%d' % (s_, t)] = 1
if os.environ.get('SEEDF'):
    d = json.load(open(os.environ['SEEDF'])); BASE.update({int(k): v for k, v in d['f'].items()}); BP.update({(int(k) if k.lstrip('-').isdigit() else k): v for k, v in d['P'].items()})
FK = COLD + CASES + [94]
PK = CASES + sorted(TX2 - set(CASES)) + ['d49'] + ['x%d_%d' % (s_, t) for s_ in RX for t in RX[s_]]


def val(f, P):
    P = dict(P)
    if not ok(f, P): return 999
    return inv(sim(f, P))


if __name__ == '__main__':
    IT = int(sys.argv[1]); random.seed(int(sys.argv[2]))
    best = (dict(BASE), dict(BP)); bs = val(*best)
    print('start', bs, flush=True)
    cur, cs = best, bs
    KEYS = [('f', k) for k in FK] + [('P', k) for k in PK]
    for rnd in range(IT):
        improved = False
        for kind, b in random.sample(KEYS, len(KEYS)):
            for v in (range(0, VMAX) if b != 'd49' else (-1, 0, 1)):
                f, P = dict(cur[0]), dict(cur[1])
                (f if kind == 'f' else P)[b] = v
                if (f, P) == cur: continue
                x = val(f, P)
                if x < cs or (x == cs and random.random() < 0.3):
                    if x < cs: improved = True
                    cur, cs = (f, P), x
        for _ in range(int(os.environ.get('MULTI', '0'))):
            f, P = dict(cur[0]), dict(cur[1])
            for _ in range(random.randint(2, 4)):
                kind, b = random.choice(KEYS); d = f if kind == 'f' else P
                d[b] = max(0 if b != 'd49' else -1, min(VMAX - 1 if b != 'd49' else 1, d.get(b, 0) + random.choice((-1, 1))))
            x = val(f, P)
            if x < cs or (x == cs and random.random() < 0.3):
                if x < cs: improved = True
                cur, cs = (f, P), x
        if cs < bs:
            bs, best = cs, (dict(cur[0]), dict(cur[1])); print(rnd, bs, flush=True)
            if bs == 0: break
        if not improved:
            f, P = dict(best[0]), dict(best[1])
            for _ in range(random.randint(2, 6)):
                kind, b = random.choice(KEYS); d = f if kind == 'f' else P
                d[b] = max(0 if b != 'd49' else -1, min(VMAX - 1 if b != 'd49' else 1, d.get(b, 0) + random.choice((-2, -1, 1, 2))))
            cur, cs = (f, P), val(f, P)
    print('best', bs, json.dumps({'f': best[0], 'P': best[1]}))
    PP = dict(best[1]); ok(best[0], PP)
    print(' '.join(map(str, sim(best[0], PP))))
