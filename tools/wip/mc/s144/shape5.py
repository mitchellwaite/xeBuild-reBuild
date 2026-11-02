# shape5.py DUMP [seed] (shape2 with env TT tail target / TP last-two prefix override) : edits = move a round-4 insert (146/128/151/79/81/69) to another trace group/position,
# with 146 key in {-1,0}; singles+pairs; plus dummy entries.
import sys, itertools, random
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
pre, g, first = r4sim.load(sys.argv[1])
import os
T = list(map(int, os.environ.get('TT', "62 33 29 69 146 128 151 35 42 53 79 81").split()))
PRE_T = list(map(int, os.environ.get('TP', "").split()))
i143 = min(first.index(143), first.index(144)) + 1 if PRE_T else first.index(143)
PREF = first[:i143+1-len(PRE_T)] + PRE_T if PRE_T else first[:i143+1]; DUM = 9999
def score(o):
    o = [b for b in o if b < DUM]
    if 143 not in o: return 99
    s = sum(a != b for a, b in zip(o[:i143+1], PREF)); j = i143
    return s + sum(a != b for a, b in zip(o[j+1:j+1+len(T)], T))
def apply(edits):
    gg = {b: list(v) for b, v in g.items()}; ov = {}
    for ed in edits:
        if ed[0] == 'M':
            _, blk, to, at, k = ed
            for b in gg:
                gg[b] = [e for e in gg[b] if not (e[0] == 'ins' and e[2] == blk)]
            L = gg[to]; gg[to] = L[:min(at, len(L))] + [('ins', 'this', blk, k)] + L[min(at, len(L)):]
        elif ed[0] == 'G':
            _, to, at, k, n = ed; L = gg[to]; gg[to] = L[:min(at, len(L))] + [('ins', 'this', DUM + n, k)] + L[min(at, len(L)):]
    try: return r4sim.sim(pre, gg, ov)
    except Exception: return []
MOV = [146, 128, 151, 79, 81]
groups = first[:i143+6]
singles = []
for blk in MOV:
    for to in groups:
        for at in range(len(g[to]) + 1):
            for k in ([-1, 0] if blk == 146 else [0]):
                singles.append(('M', blk, to, at, k))
for to in groups:
    for at in range(len(g[to]) + 1):
        for k in [-2, -1, 0]:
            singles.append(('G', to, at, k, 0))
res = []
for s in singles:
    o = apply([s]); res.append((score(o), [s]))
res.sort(key=lambda r: r[0]); print('singles', len(singles), res[:8], flush=True)
top = [r[1][0] for r in res[:300]]
pres = []
for a, b in itertools.combinations(top, 2):
    o = apply([a, b]); pres.append((score(o), [a, b]))
pres.sort(key=lambda r: r[0]); print('pairs', pres[:8], flush=True)
# SA over edit sets
random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
cur = list(pres[0][1]); cs = pres[0][0]; best = (cs, cur)
for it in range(20000):
    nxt = list(cur); r = random.random()
    if r < 0.4 or not nxt: nxt.append(random.choice(singles))
    elif r < 0.7: nxt.pop(random.randrange(len(nxt)))
    else: nxt[random.randrange(len(nxt))] = random.choice(singles)
    nxt = nxt[:5]; s = score(apply(nxt)); t = max(0.05, 1.5 * (1 - it / 20000))
    if s <= cs or random.random() < 2.718 ** ((cs - s) / t):
        cur, cs = nxt, s
        if s < best[0]: best = (s, list(nxt)); print('sa', best, flush=True)
    if best[0] == 0: break
print('best', best, [b for b in apply(best[1]) if b < DUM][i143+1:i143+14])
