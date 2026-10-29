"""anneal2.py START.txt EVALS SEED : annealing over f/P values AND the zero-flow asm-goto target orders
(X1ORD: vY asm goto, X2ORD: rok asm goto).  START.txt = a pfxsearch output line.  env as fake7."""
import os, sys, json, random, math
src, EV, SEED = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sys.argv = ['x', '0', '1']
import fake7
random.seed(SEED)
l = [x for x in open(src) if 'X2ORD=' in x][-1].split(' ', 4)
X2 = [int(x) for x in l[2].split('=')[1].split(',') if x]
X1 = [int(x) for x in l[3].split('=')[1].split(',') if x]
d = json.loads(l[4])
f0 = {int(k): v for k, v in d['f'].items()}
P0 = {(int(k) if k.lstrip('-').isdigit() else k): v for k, v in d['P'].items()}
X1ALL = [112, 115, 121, 107, 108, 109, 116, 119, 120, 128, 129, 132, 117, 130, 103]
FK = [k for k in f0 if k != 94] + [94]
PK = [k for k in P0 if k not in ('x126_125',)]
RXF = os.environ.get('RXF', '1') == '1'


def val(st):
    f, P, x1, x2 = st
    fake7.X1ORD, fake7.X2ORD = x1, x2
    P = dict(P)
    if RXF and P.get('x126_125', 0): P['x126_125'] = (f[126] + 1) // 2
    PP = dict(P)
    if not fake7.ok(f, PP): return 999
    return fake7.inv(fake7.sim(f, PP))


def move(st):
    f, P, x1, x2 = dict(st[0]), dict(st[1]), list(st[2]), list(st[3])
    r = random.random()
    if r < 0.35:
        b = random.choice(FK); f[b] = max(0, min(10, f[b] + random.choice((-1, 1))))
    elif r < 0.55:
        b = random.choice(PK)
        lo, hi = (-1, 0) if b == 'd49' else (0, 10)
        P[b] = max(lo, min(hi, P.get(b, 0) + random.choice((-1, 1))))
    elif r < 0.7:
        i, j = random.randrange(len(x2)), random.randrange(len(x2)); x2[i], x2[j] = x2[j], x2[i]
    elif r < 0.85:
        if x1 and random.random() < 0.5:
            i, j = random.randrange(len(x1)), random.randrange(len(x1)); x1[i], x1[j] = x1[j], x1[i]
        else:
            t = random.choice(X1ALL)
            if t in x1: x1.remove(t)
            else: x1.insert(random.randrange(len(x1) + 1), t)
    else:
        P['x126_125'] = 0 if P.get('x126_125') else 1
        if random.random() < 0.5: P['x117_130'] = 0 if P.get('x117_130') else 1
    return (f, P, x1, x2)


cur = (f0, P0, X1, X2); cs = val(cur); best, bs = cur, cs
print('start', cs, flush=True)
T0 = float(os.environ.get('T0', '1.0'))
for i in range(EV):
    T = T0 * (1 - i / EV) + 0.05
    nx = move(cur)
    if random.random() < 0.3: nx = move(nx)
    x = val(nx)
    if x >= 998: continue
    if x <= cs or random.random() < math.exp((cs - x) / T):
        cur, cs = nx, x
        if x < bs:
            best, bs = nx, x
            print(i, bs, 'X2ORD=' + ','.join(map(str, best[3])), 'X1ORD=' + ','.join(map(str, best[2])),
                  json.dumps({'f': best[0], 'P': best[1]}), flush=True)
            if bs == 0: break
print('best', bs)
