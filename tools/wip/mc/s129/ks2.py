import sys, random, difflib
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86')
import r4sim
pre, g, first = r4sim.load('d_pm/mc.bbro')
T = [112,115,103,55,126,125,61,33,29,67,127,130,117]
def score(o):
    o = o[o.index(49)+1:]; o = o[:o.index(67)+4]
    sm = difflib.SequenceMatcher(None, o, T, autojunk=False)
    return len(T) + len(o) - 2*sum(b.size for b in sm.get_matching_blocks())
BL = [103,112,115,125,126,127,130,117,33,29,53]
base = {}
best = []
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
for it in range(20000):
    n = random.randint(1, 4); ov = {b: random.randint(-6, 0) for b in random.sample(BL, n)}
    try: o = r4sim.sim(pre, g, ov)
    except Exception: continue
    s = score(o); best.append((s, len(ov), sorted(ov.items()), o[o.index(49)+1:o.index(49)+18]))
best.sort(key=lambda x: (x[0], x[1]))
seen=set()
for x in best[:400]:
    if str(x[2]) in seen: continue
    seen.add(str(x[2])); print(x)
    if len(seen) > 12: break
