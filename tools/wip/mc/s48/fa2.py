"""fa2.py SLOT: 77/79 moved into 61 (79,77 after pos 2) + random hill climb of freq overrides and 55/126/125 ins relocation."""
import sys, random, copy
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s48')
from fs import tinv, hsim, R
from wi10 import strip
R1 = copy.deepcopy(R); g = R1[3]['g']
e7 = strip(g, 77); e9 = strip(g, 79); g[61] = g[61][:2] + [e9, e7] + g[61][2:]
print('mv', tinv(hsim.sim(R1, {}, {})))
B = [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
random.seed(2); best = 99
for rs in range(40):
    f = {}; cur = 99
    for it in range(400):
        h = dict(f); b = random.choice(B); h[b] = random.randint(0, 6)
        if not h[b]: h.pop(b)
        v = tinv(hsim.sim(R1, h, {}))
        if v <= cur: f, cur = h, v
    if cur < best: best = cur; print(cur, f, [x for x in hsim.sim(R1, f, {}) if x in B], flush=True)
