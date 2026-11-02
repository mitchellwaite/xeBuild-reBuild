"""fa.py SLOT: random-restart hill climb of freq overrides (0..6) on round-4 named blocks; min true inv."""
import sys, random
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s48')
from fs import tinv, hsim, R
B = [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
best = (99, None); random.seed(1)
for rs in range(30):
    f = {}; cur = tinv(hsim.sim(R, f, {}))
    for it in range(400):
        g = dict(f); b = random.choice(B); g[b] = random.randint(0, 6)
        if g[b] == 0: g.pop(b)
        v = tinv(hsim.sim(R, g, {}))
        if v <= cur: f, cur = g, v
    if cur < best[0]: best = (cur, f); print(best, flush=True)
