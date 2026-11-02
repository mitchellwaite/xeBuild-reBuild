# alt.py DUMP [maxk] : enumerate alternative change sets on r4 shape (dummies, key overrides, removals)
import sys, itertools, time
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
pre, g, first = r4sim.load(sys.argv[1]); MAXK = int(sys.argv[2]) if len(sys.argv) > 2 else 2
D = 9999
i = first.index(150); TGT = first[:i] + [147,128,150,35,42,53,79,81] + first[i+8:]
def score(o):
    o = [b for b in o if b < D]
    return sum(a != b for a, b in zip(o, TGT)) + abs(len(o) - len(TGT))
TAIL = [150,147,79,128,81,42,53,35,144,145,75]
CH = []
for G in first:
    for at in range(len(g[G]) + 1):
        for k in (0, -1, -2):
            CH.append(('dum', G, at, k))
for b in TAIL:
    for k in (-2, -1, 1):
        CH.append(('key', b, k))
for G in first:
    for j, e in enumerate(g[G]):
        if e[0] in ('ins', 'chg'): CH.append(('rm', G, j))
def run(cs):
    gg = {b: list(v) for b, v in g.items()}; ov = {}
    rms = sorted([c for c in cs if c[0] == 'rm'], key=lambda c: -c[2])
    for c in rms: gg[c[1]] = gg[c[1]][:c[2]] + gg[c[1]][c[2]+1:]
    # dummies applied on original indices: offset after removals is approximate; apply removal-free groups
    dms = sorted([c for c in cs if c[0] == 'dum'], key=lambda c: -c[2])
    for n, c in enumerate(dms):
        L = gg[c[1]]; gg[c[1]] = L[:c[2]] + [('ins', 'this', D + n, c[3])] + L[c[2]:]
    for c in cs:
        if c[0] == 'key': ov[c[1]] = c[2]
    try: return r4sim.sim(pre, gg, ov)
    except Exception: return []
def ok(cs):
    if sum(c[0]=='dum' for c in cs) > 3: return False
    if len({c[1] for c in cs if c[0]=='key'}) < sum(c[0]=='key' for c in cs): return False
    gr = [c[1] for c in cs if c[0]=='rm']; 
    if gr and any(c[0]=='dum' and c[1] in gr for c in cs): return False
    return True
print('base', score(run([])), 'nch', len(CH)); sys.stdout.flush()
best = {}
t = time.time()
for n in range(1, MAXK + 1):
    for cs in itertools.combinations(CH, n):
        if not ok(cs): continue
        s = score(run(list(cs)))
        if s <= 2: print(n, s, cs); sys.stdout.flush()
    print('done', n, time.time() - t); sys.stdout.flush()
