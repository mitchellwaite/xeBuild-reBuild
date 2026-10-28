"""htail.py SLOTDIR [b=f/P ...] : exhaustive nonincreasing tail enumeration on a real history (hsim)."""
import sys, itertools, json
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\wip\mc\s18')
import hsim, fake7
R, keys = hsim.load(sys.argv[1])
f0, P0 = hsim.measured(keys)
for a in sys.argv[2:]:
    b, v = a.split('='); fv, pv = v.split('/'); f0[int(b)] = int(fv); P0[int(b)] = int(pv)
TAIL = [55, 126, 61, 33, 29, 67, 127, 117, 35, 42, 53, 77, 79]
top = fake7.rmax((f0[49] + .5) / 2)
best = 99; n = 0
for comb in itertools.combinations_with_replacement(range(top, -1, -1), len(TAIL)):
    fx = dict(zip(TAIL, comb)); fx[49] = f0[49]
    if not fake7.chain_ok(fx): continue
    for v125 in range(top + 1):
        for v130 in range(3):
            f = dict(f0); f.update(fx); f[125] = v125; f[130] = v130
            P = dict(P0)
            if P.get(125): P[125] = (f[126] + 1) // 2
            if P[125] > f[125]: continue
            n += 1
            x = hsim.inv(hsim.sim(R, f, P))
            if x < best or x == 0:
                best = x; print(x, json.dumps({b: f[b] for b in TAIL + [125, 130]}), 'P125', P.get(125), flush=True)
print('done', n, best)
