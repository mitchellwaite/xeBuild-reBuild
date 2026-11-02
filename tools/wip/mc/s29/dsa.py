"""dsa.py OUT SEED ITERS [init.json]: SA over des.py designs (rok/x1 JMP chains, rx, t48), real compiles.
score = true inversions + 3 if k94 is not right after 129 (+5 per missing tail block)."""
import sys, json, random, math, des, ev
out, seed, iters = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
L = ['c12', 'c11', 'p0', 'i0', 'c9', 'hdd4', 'hdd5', 'c2', 'c1', 'c10', 'u2', 'cdef', 'c8', 'c7', 'c3', 's5', 's4', 'p1', 'i1', 'h4t', 'h5t']
def spec(ch): return ';'.join(','.join(j) for j in ch if j)
def score(st):
    sc, r = des.run('dsa%d' % seed, rok=spec(st['rok']), x1=spec(st['x1']), rx=st['rx'], t48=st['t48'])
    if sc is None: return 999, ''
    tok = r['order'].split()[1:]
    s, miss, o = ev.score_order(tok)
    s += 5 * len([b for b in miss if b not in ev.CASES])
    if '129' in tok and 'k94' in tok:
        if tok.index('k94') != tok.index('129') + 1: s += 3
    elif 'k94' in tok: s += 3
    return s, r['order']
def mut(st):
    st = json.loads(json.dumps(st)); k = random.random()
    if k < 0.9:
        site = 'rok' if random.random() < 0.65 else 'x1'
        lv = random.randrange(3); j = st[site][lv]; x = random.choice(L)
        if x in j: j.remove(x)
        else: j.insert(random.randint(0, len(j)), x)
    elif k < 0.95: st['rx'] = not st['rx']
    else: st['t48'] = not st['t48']
    return st
random.seed(seed)
st = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {'rok': [[], [], []], 'x1': [[], [], []], 'rx': True, 't48': True}
cur, o = score(st); best = cur; T = 4.0
fo = open(out, 'a'); print('start', cur, o, flush=True)
for it in range(iters):
    nst = mut(st)
    while random.random() < 0.4: nst = mut(nst)
    x, o = score(nst)
    fo.write(json.dumps([x, nst, o]) + '\n'); fo.flush()
    if x <= cur or random.random() < math.exp((cur - x) / T): st, cur = nst, x
    if x < best: best = x; print(it, x, json.dumps(nst), o, flush=True)
    T = max(0.7, T * 0.999)
