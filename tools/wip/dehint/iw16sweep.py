"""python tools/wip/dehint/iw16sweep.py <gen_iwN.py> [-n top] [-t threads]: cross product of a generator's AXES (base from IWB or the generator's BASE, plain -O3), scored by lines and compare
signature. Prints the histogram of signatures with the best lines for each, the top states, and every state with the full target signature `<>>><<<<` (source saved to build/iw/a16/<gen>_<label>.c)."""
import collections, hashlib, importlib.util, itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib, iw16rej
a = sys.argv[1:]
top = 12; th = 2
if '-n' in a:
    i = a.index('-n'); top = int(a[i + 1]); del a[i:i + 2]
if '-t' in a:
    i = a.index('-t'); th = int(a[i + 1]); del a[i:i + 2]
sp = importlib.util.spec_from_file_location('g', a[0]); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
base = getattr(m, 'BASE', os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a15_dead.c'))
base = os.environ.get('IWB', base)
text = open(os.path.join(iwlib.R, base), newline='').read().replace('\r\n', '\n')
gen = os.path.splitext(os.path.basename(a[0]))[0]
combos = list(itertools.product(*m.AXES))
if hasattr(m, 'FILTER'):
    combos = [c for c in combos if m.FILTER(c)]
print(len(combos), 'variants', flush=True)
def one(c):
    lab = '+'.join(x[0] for x in c if x[0])
    t = text
    for l, ed in c:
        for x, y in ed:
            if x not in t:
                return lab, None, 'missing %s %r' % (l, x[:50]), t
            t = t.replace(x, y)
    r, s = iw16rej.sigscore(t)
    return lab, r, s, t
res = list(ThreadPoolExecutor(th).map(one, combos))
bad = [r for r in res if r[1] is None or 'compile' in r[1]]
good = [r for r in res if r[1] is not None and 'compile' not in r[1]]
good.sort(key=lambda r: r[1]['total'])
if bad:
    print(len(bad), 'failed, first:', bad[0][0], bad[0][2] if bad[0][1] is None else bad[0][1]['compile'][:200])
h = collections.defaultdict(lambda: [0, 1e9, ''])
for lab, r, s, t in good:
    e = h[r.get('sig8')]; e[0] += 1
    if r['total'] < e[1]:
        e[1] = r['total']; e[2] = lab
for s, e in sorted(h.items(), key=lambda kv: kv[1][1]):
    print('sig', s, 'n', e[0], 'best', e[1], e[2])
for lab, r, s, t in good[:top]:
    print(r['total'], s, r.get('sig8'), lab, iwlib.fmt(r)[:110])
for lab, r, s, t in good:
    if r.get('sig8') == iw16rej.TARGET8 or r['total'] == 0:
        print('TARGET', r['total'], lab, iwlib.fmt(r)[:110])
        # the hash: Windows names ignore case, so labels like L3re1 and L3Re1 would collide
        p = os.path.join(iw16rej.OUT, '%s_%s_%s.c' % (gen, lab.replace('+', '_')[:60], hashlib.md5(t.encode()).hexdigest()[:6]))
        open(p, 'w', newline='\n').write(t)
if good:
    open(os.path.join(iw16rej.OUT, gen + '_best.c'), 'w', newline='\n').write(good[0][3])
