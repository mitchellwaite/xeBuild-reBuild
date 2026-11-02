"""psa.py TAG seed: SA over case f (P fixed as measured unless PFREE) + tail f/P on TAG history; 94 must follow 129."""
import sys, os, random, math
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot, mcsim2
mcsim2.pos[94] = 999
Rr, keys = hsim.load(os.path.join(R0, 'build', 'v', 'mc29', 'slot_' + sys.argv[1]))
f0, P0 = hsim.measured(keys)
hsim.RXEV.update({126: [125], 117: [130]})
CS = [b for b in [129, 107, 110, 113, 108, 119, 120, 121, 128, 116, 132] if b in f0]
TL = [b for b in [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79] if b in f0]
PB = [b for b in [49, 112, 115, 103, 125, 130, 117, 132, 94, 129] if b in f0]
def sc(f, P):
    o = hsim.sim(Rr, f, P)
    s = pot.tinv([b for b in o if b != 94])
    if 94 in o and 129 in o and o.index(94) != o.index(129) + 1: s += 3
    return s, o
random.seed(int(sys.argv[2]))
f, P = dict(f0), dict(P0); cur, o = sc(f, P); best = (cur, f, P, o); T = 2
for it in range(int(sys.argv[3]) if len(sys.argv) > 3 else 8000):
    g, Q = dict(f), dict(P)
    for _ in range(random.choice([1, 1, 2])):
        r = random.random()
        if r < 0.4: b = random.choice(CS); g[b] = max(4, min(10, g[b] + random.choice([-1, 1])))
        elif r < 0.8: b = random.choice(TL); g[b] = max(0, min(9, g[b] + random.choice([-1, 1])))
        else: b = random.choice(PB); Q[b] = max(0, min(10, Q.get(b, 0) + random.choice([-1, 1])))
    x, o2 = sc(g, Q)
    if x <= cur or random.random() < math.exp((cur - x) / T): f, P, cur = g, Q, x
    if cur < best[0]: best = (cur, dict(f), dict(P), o2)
    T = max(0.3, T * 0.9995)
    if cur == 0: break
print('BEST', best[0], {b: best[1][b] for b in best[1] if best[1][b] != f0.get(b)}, {b: best[2][b] for b in best[2] if best[2][b] != P0.get(b)}, best[3])
