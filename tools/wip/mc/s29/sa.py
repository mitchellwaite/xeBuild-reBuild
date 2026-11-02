"""sa.py TAG S RX seed : simulated annealing over f (BL) and P (PB) on TAG history edited with ed5.edit(S)."""
import sys, random, math
tag, S, rx, seed = sys.argv[1], tuple(int(x) for x in sys.argv[2].split(",") if x), sys.argv[3], int(sys.argv[4])
sys.argv = ['x', tag]
import ed5, hsim, pot
AT = int(sys.argv[6]) if len(sys.argv) > 6 else 1102
Rx = ed5.edit(S, AT) if S != (0,) else ed5.Rr
hsim.RXEV.clear()
for it in rx.split(','):
    if it: s, t = map(int, it.split(':')); hsim.RXEV.setdefault(s, []).append(t)
BL = [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
BL += [int(x) for x in __import__("os").environ.get("BLX", "").split(",") if x]
PB = [49, 112, 115, 103, 125, 130, 117] + [int(x) for x in __import__("os").environ.get("PBX", "").split(",") if x]
random.seed(seed)
f = dict(ed5.f0); P = dict(ed5.P0)
for b in S: P[b] = P.get(b) or 1
P[49] = 1
def sc(f, P): return pot.tinv(hsim.sim(Rx, f, P))
cur = sc(f, P); best = (cur, dict(f), dict(P)); T = 2.0
for it in range(int(sys.argv[5]) if len(sys.argv) > 5 else 6000):
    g, Q = dict(f), dict(P)
    for _ in range(random.choice([1, 1, 2, 3])):
        if random.random() < 0.75: b = random.choice(BL); g[b] = max(0, min(9, g[b] + random.choice([-2, -1, 1, 2])))
        else: b = random.choice(PB); Q[b] = max(0, min(int(__import__("os").environ.get("PMAX", "5")), Q.get(b, 0) + random.choice([-1, 1])))
    x = sc(g, Q)
    if x <= cur or random.random() < math.exp((cur - x) / T): f, P, cur = g, Q, x
    if cur < best[0]: best = (cur, dict(f), dict(P)); print(it, cur, flush=True)
    if cur == 0: break
    T = max(0.3, T * 0.9995)
print('BEST', best[0], {b: best[1][b] for b in BL if best[1][b] != ed5.f0.get(b)}, {b: best[2].get(b) for b in PB})
