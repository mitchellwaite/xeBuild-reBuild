"""python tools/wip/dehint/irsweep.py <gen_irN.py> [-n TOP] [-k label]

A generator module defines:
  AXES = [ [ (label, [(old, new), ...]), ... ], ... ]   cross product of source edits
  BASE (optional)  source file, relative to the repo root, default src/image_read.c
  REMOVE (optional): names from irtricks.T to apply first
  FOCUS (optional) list of functions: sort key counts only these
Prints the TOP best variants. -k label writes the variant with that label joined by '+' to
build/ir/<gen>_best.c (the best one is written there by default)."""
import importlib.util, itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib, irtricks


def load(p):
    s = importlib.util.spec_from_file_location('gen', p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def build(text, combo):
    for label, edits in combo:
        for a, b in edits:
            if a not in text:
                raise ValueError('edit in %s not found: %r' % (label, a[:70]))
            text = text.replace(a, b)
    return text


def main():
    a = sys.argv[1:]
    top = 25
    keep = None
    if '-n' in a:
        i = a.index('-n')
        top = int(a[i + 1])
        del a[i:i + 2]
    if '-k' in a:
        i = a.index('-k')
        keep = a[i + 1]
        del a[i:i + 2]
    gen = a[0]
    m = load(gen)
    base = getattr(m, 'BASE', 'src/image_read.c')
    text = open(os.path.join(irlib.R, base), newline='').read().replace('\r\n', '\n')
    text = irtricks.apply(text, getattr(m, 'REMOVE', []))
    focus = getattr(m, 'FOCUS', None)
    combos = list(itertools.product(*m.AXES))
    print(len(combos), 'variants', flush=True)

    def one(c):
        lab = '+'.join(x[0] for x in c if x[0])
        try:
            t = build(text, c)
        except ValueError as e:
            return lab, {'compile': str(e)}, 1e9, None
        r = irlib.score_text(t, [])
        if 'compile' in r:
            return lab, r, 1e9, t
        if focus:
            k = sum(v for n, v in r['per'].items() if n in focus)
        else:
            k = r['total']
        return lab, r, k, t
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(one, combos))
    res.sort(key=lambda x: (x[2], x[1].get('total', 0)))
    for lab, r, k, t in res[:top]:
        print(k, '|', lab or '(base)', '|', irlib.fmt(r)[:200])
    name = os.path.splitext(os.path.basename(gen))[0]
    out = os.path.join(irlib.BUILD, name + '_best.c')
    pick = res[0]
    if keep is not None:
        pick = [x for x in res if x[0] == keep][0]
    if pick[3]:
        open(out, 'w', newline='\n').write(pick[3])
        print('wrote', out, 'from', pick[0])


main()
