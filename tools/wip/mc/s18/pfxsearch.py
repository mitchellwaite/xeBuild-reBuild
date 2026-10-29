"""pfxsearch.py N SEED : random strict prefix designs (distinct decreasing keys for cases..103),
random X2 label order and f94, each followed by the exhaustive tail enumeration.  env as fake7
(must include X2CASES=1, RX=126:125,117:130).  Prints any design reaching a new best."""
import os, sys, json, random, itertools
N, SEED = int(sys.argv[1]), int(sys.argv[2])
sys.argv = ['x', '0', '1']
import fake7
random.seed(SEED)
ORDER = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116, 132, 49, 112, 115, 103]
FMAX = int(os.environ.get('FMAX', '9'))
TAIL = [55, 126, 61, 33, 29, 67, 127, 117, 35, 42, 53, 77, 79]


def prefix():
    """walk ORDER with strictly decreasing keys 100P+f"""
    for _ in range(2000):
        f, P = {}, {}
        hi = 100 * 10 + 11
        ok = True
        tie = float(os.environ.get('TIE', '0'))
        for b in ORDER:
            cands = []
            for p in range(1, 11):
                for v in range(p, FMAX + 1):
                    k = 100 * p + v
                    if k > hi or (k == hi and not (random.random() < tie and b in fake7.CASES)): continue
                    if b in (110, 113) and v != p: continue
                    if b in fake7.CASES and b not in (110, 113, 121, 132) and v - p > p: continue
                    if b == 132 and not (p <= v <= 3 * p and p <= fake7.P132MAX): continue
                    if b in (112, 115, 103) and (p > 4 or v > 9 or (b == 103 and v < p + 1)): continue
                    if b in fake7.CASES and v > fake7.FMAX: continue
                    if b == 49 and not ((v - 1 if os.environ.get('D49') == '1' else v) <= p <= v): continue
                    cands.append((k, p, v))
            if not cands: ok = False; break
            # prefer keys close below hi so the chain does not run out
            cands.sort(reverse=True)
            if b == 49:
                c49 = [c for c in cands if c[2] >= int(os.environ.get('F49MIN', '5'))]
                if not c49: ok = False; break
                k, p, v = random.choice(c49[:3])
            else:
                top = cands[:max(1, random.choice((1, 2, 2, 3, 4, 6)))]
                if random.random() < 0.6:
                    lowf = [c for c in top if c[2] == c[1]]
                    top = lowf or top
                k, p, v = random.choice(top)
            hi = k
            f[b] = v; P[b] = p
        if ok:
            P['d49'] = P.pop(49) - f[49]
            return f, P
    return None


best = 99
for it in range(N):
    r = prefix()
    if not r: continue
    f0, P0 = r
    f0[94] = random.randint(max(0, 10 - f0[49]), 9)
    order2 = [112, 115, 103] + random.sample([107, 108, 109, 119, 120, 121, 128, 129, 116, 132], 10) + random.sample([117, 130], 2)
    random.shuffle(order2)
    fake7.X2ORD = [t for t in order2 if t in fake7.TX2]
    if os.environ.get('RX1') == '1':
        x1 = [t for t in [112, 115, 121, 107, 108, 109, 116, 119, 120, 128, 129, 132, 117, 130, 103] if random.random() < 0.5]
        random.shuffle(x1); fake7.X1ORD = x1
    top = fake7.rmax((f0[49] + .5) / 2)
    for comb in itertools.combinations_with_replacement(range(top, -1, -1), len(TAIL)):
        fx = dict(zip(TAIL, comb)); fx[49] = f0[49]
        if not fake7.chain_ok(fx): continue
        for v125 in range(top + 1):
            for v130 in range(3):
                for xr, xq in ((0, 0), (1, 0), (0, 1), (1, 1)):
                    f = dict(f0); P = dict(P0)
                    for b, v in zip(TAIL, comb): f[b] = v
                    f[125] = v125; f[130] = v130
                    P['x126_125'] = (f[126] + 1) // 2 if xr else 0; P['x117_130'] = xq
                    for t in (117, 130): P[t] = 0
                    PP = dict(P)
                    if not fake7.ok(f, PP): continue
                    x = fake7.inv(fake7.sim(f, PP))
                    if x < best or x == 0:
                        best = x
                        print(it, x, 'X2ORD=' + ','.join(map(str, fake7.X2ORD)), 'X1ORD=' + ','.join(map(str, fake7.X1ORD or [])), json.dumps({'f': f, 'P': P}), flush=True)
print('done', best)
