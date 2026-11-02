"""hsa.py SLOTTAG ITERS: SA over tail f (and P) on a real history; prints best inv + needed deltas."""
import sys, os, random, math
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); import hsim
R, keys = hsim.load(os.path.join(R0, 'build', 'v', 'mc37', 'slot_' + sys.argv[1]))
f0, P0 = hsim.measured(keys)
BL = [b for b in [115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79] if b in f0]
sc = lambda f: hsim.inv(hsim.sim(R, f, P0))
random.seed(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
f = dict(f0); cur = sc(f); best = (cur, dict(f)); T = 2.0
print('measured', cur)
for it in range(int(sys.argv[2])):
    g = dict(f); b = random.choice(BL); g[b] = max(0, min(10, g[b] + random.choice([-1, 1])))
    s = sc(g) + 0.2 * sum(abs(g[x] - f0[x]) for x in BL)
    c = cur + 0.2 * sum(abs(f[x] - f0[x]) for x in BL)
    if s <= c or random.random() < math.exp((c - s) / T): f, cur = g, sc(g)
    if cur < best[0] or (cur == best[0] and sum(abs(f[x]-f0[x]) for x in BL) < sum(abs(best[1][x]-f0[x]) for x in BL)): best = (cur, dict(f))
    T = max(0.05, T * 0.999)
print('best', best[0], {b: (f0[b], best[1][b]) for b in BL if best[1][b] != f0[b]})
