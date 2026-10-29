"""grid.py SLOT 'key=v1,v2,..' ... [--show b,b,..] : compile combos from <MCD>/slot<SLOT>/ov.json, print measured keys."""
import sys, json, os, itertools
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import runq, analyze
from concurrent.futures import ThreadPoolExecutor
MCD = os.environ['MCD']; ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
slot = sys.argv[1]
args = sys.argv[2:]
show = [49, 55, 61, 103]
if '--show' in args:
    i = args.index('--show'); show = [int(x) if x.isdigit() else x for x in args[i + 1].split(',')]; args = args[:i]
base = json.load(open(r'%s\build\%s\slot%s\ov.json' % (ROOT, MCD, slot)))
axes = [(a.split('=')[0], [float(x) for x in a.split('=')[1].split(',')]) for a in args]
combos = list(itertools.product(*[v for _, v in axes]))
def run(ic):
    i, c = ic
    ov = dict(base)
    for (k, _), v in zip(axes, c): ov[k] = v
    s = '%s_g%d' % (slot, i % 4)
    fn, out = runq.compile_(s, ov)
    o, inv, keys, named = analyze.analyze(r'%s\build\%s\slot%s' % (ROOT, MCD, s))
    return c, fn, runq.content(r'%s\build\%s\slot%s' % (ROOT, MCD, s)), inv, [keys.get(b, named.get(b)) for b in show]
for ch in range(0, len(combos), 4):
    with ThreadPoolExecutor(4) as ex:
        for c, fn, ct, inv, ks in ex.map(run, list(enumerate(combos))[ch:ch + 4]):
            print(' '.join('%.3f' % x for x in c), 'fncmp', fn, 'content', ct, 'inv', inv, ' '.join('%s=%s' % (b, k) for b, k in zip(show, ks)), flush=True)
