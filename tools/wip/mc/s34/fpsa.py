"""fpsa.py TAG ITERS SEED [PFREE=1]: SA over tail f (0..10) and P (0..6) on TAG's real history (hsim); score pot.tinv + 0.1*L1."""
import sys, os, random, math
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
R, keys = hsim.load(os.path.join(R0, 'build', 'v', 'mc34', 'slot_' + sys.argv[1]))
f0, P0 = hsim.measured(keys)
BL = [b for b in [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79] if b in f0]
PF = len(sys.argv) > 4 and sys.argv[4] == '1'
random.seed(int(sys.argv[3]))
def sc(f, P): return pot.tinv(hsim.sim(R, f, P))
def L(f, P): return sum(abs(f[b] - f0[b]) for b in BL) + sum(abs(P.get(b, 0) - P0.get(b, 0)) for b in BL)
f, P = dict(f0), dict(P0); cur = sc(f, P); best = (cur, 0, f, P); T = 3.0
for it in range(int(sys.argv[2])):
    g, Q = dict(f), dict(P); b = random.choice(BL)
    if PF and random.random() < 0.35: Q[b] = max(0, min(6, Q.get(b, 0) + random.choice([-1, 1])))
    else: g[b] = max(0, min(10, g[b] + random.choice([-1, 1])))
    try: s = sc(g, Q)
    except Exception: continue
    if s + 0.1 * L(g, Q) <= cur + 0.1 * L(f, P) or random.random() < math.exp((cur + 0.1 * L(f, P) - s - 0.1 * L(g, Q)) / T): f, P, cur = g, Q, s
    if (cur, L(f, P)) < best[:2]: best = (cur, L(f, P), dict(f), dict(P))
    T = max(0.05, T * (1 - 4.0 / int(sys.argv[2])))
f, P = best[2], best[3]
print('best', best[0], 'L1', best[1], 'df', {b: (f0[b], f[b]) for b in BL if f[b] != f0[b]}, 'dP', {b: (P0.get(b, 0), P.get(b, 0)) for b in BL if P.get(b, 0) != P0.get(b, 0)})
print(' ', ' '.join(map(str, hsim.sim(R, f, P)[11:])))
