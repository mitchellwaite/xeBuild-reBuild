"""hanneal.py SLOTDIR EVALS SEED : annealing over design f/P values on a real history (hsim).
Prints improvements as json designs (f, P with P[125] forced from f[126], P49 in {f49-1, f49})."""
import sys, json, random, math, os
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import hsim, fake7
sd, EV, SEED = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
random.seed(SEED)
R, keys = hsim.load(sd)
f0, P0 = hsim.measured(keys)
f0.update(hsim.armf(sd))
if os.environ.get('START'):
    d = json.load(open(os.environ['START']))
    for k, v in d['f'].items(): f0.setdefault(int(k), v)
    for k, v in d['P'].items():
        if k.lstrip('-').isdigit(): P0.setdefault(int(k), v)
    if 'd49' in d['P']: P0.setdefault(49, d['f']['49'] + d['P']['d49'])
CASES = fake7.CASES
TAIL = [55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
FMAX = int(os.environ.get('FMAX', '10'))
LOCK = set(int(x) for x in os.environ.get('LOCK', '').split(',') if x)   # blocks whose f/P stay as measured
RX126 = P0.get(125, 0) > 0
RX117 = '117:130' in os.environ.get('RXEV', '')


MARG = float(os.environ.get('MARG', '0.3'))


def chain_ok(f):
    rm = fake7.rmax
    x49 = f[49] + MARG
    h = 0.48
    return f[55] <= rm(x49 * h) and f[61] <= rm(x49 * h * h) and f[67] <= rm(x49 * h ** 3)         and f[61] <= rm((f[55] + MARG) * h) and f[67] <= rm((f[61] + MARG) * h)


def ok(f, P):
    if not chain_ok(f): return False
    if not (f[49] - 1 <= P[49] <= f[49]): return False
    if f[94] > 9 or f[94] + f[49] < int(os.environ.get('F48', '15')) or P.get(94, f[94]) != f[94]: return False
    for c in CASES:
        if f[c] > FMAX or P[c] < 1 or P[c] > f[c]: return False
        if c in (110, 113) and f[c] != P[c]: return False
        if c == 132:
            if f[c] > 3 * P[c]: return False
        elif f[c] - P[c] > P[c]: return False
    for b in (112, 115, 103):
        if P[b] > f[b] or f[b] > 9: return False
    if f[103] < P[103] + 1: return False
    if f[103] - P[103] > int(os.environ.get('U2BASE', '99')): return False
    if f[112] - P[112] > f[110] / 2 or f[115] - P[115] > f[113] / 2: return False
    if f[117] > f[116] / 2 or f[130] > f[129] / 2 or f[127] > f[121] / 2: return False
    if RX117:
        if P.get(130, 0) > f[130] + 1 or (P.get(130, 0) and f[117] < 1): return False
    elif P.get(130, 0): return False
    if max(f[b] for b in TAIL) > 9: return False
    if f[127] > f[121] or f[126] > f[121] / 2 + .5: return False
    if RX126 and P[125] > f[125]: return False
    if sum(f[c] for c in CASES) + P[112] + P[115] + P[103] > int(os.environ.get('FLOWMAX', '113')): return False
    sp = sum(P[c] for c in CASES)
    if sum(f[c] - P[c] for c in CASES if c != 132) + P[112] + P[115] + P[103] + max(0, sp - int(os.environ.get('DMAX', '78'))) > int(os.environ.get('X2MAX', '31')): return False
    if f[126] > (f[121] - f[127]) * 0.48 + 0.3: return False
    return True


def val(f, P):
    P = dict(P)
    if RX126: P[125] = (f[126] + 1) // 2
    if not ok(f, P): return 999
    return hsim.inv(hsim.sim(R, f, P))


FK = [b for b in CASES + [49, 112, 115, 103, 94] + TAIL if b not in LOCK]
PK = [b for b in CASES + [49, 112, 115, 103] + ([130] if RX117 else []) if b not in LOCK]
cur = (dict(f0), dict(P0)); cs = val(*cur); best, bs = cur, cs
print('start', cs, flush=True)
T0 = float(os.environ.get('T0', '1.0'))
for i in range(EV):
    T = T0 * (1 - i / EV) + 0.05
    f, P = dict(cur[0]), dict(cur[1])
    for _ in range(random.choice((1, 1, 2, 3))):
        if random.random() < 0.6:
            b = random.choice(FK); f[b] = max(0, min(10, f[b] + random.choice((-1, 1))))
            if b == 94: P[94] = f[94]
        else:
            b = random.choice(PK); P[b] = max(0, min(10, P[b] + random.choice((-1, 1))))
    x = val(f, P)
    if x >= 998: continue
    if x <= cs or random.random() < math.exp((cs - x) / T):
        cur, cs = (f, P), x
        if x < bs:
            best, bs = (f, P), x
            print(i, bs, json.dumps({'f': f, 'P': P}), flush=True)
            if bs == 0: break
print('best', bs)
