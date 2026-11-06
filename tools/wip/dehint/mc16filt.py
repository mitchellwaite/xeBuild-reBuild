"""mode_client attempt 16: mc14filt with k up to 8 (mc15k.add) and a slice of the variant
list, so a stopped sweep can be resumed.

python tools/wip/dehint/mc16filt.py BASE_k0.c -g FAMILIES [-from N] [-to M] [-j 4] [-o DIR]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc14filt, mc15k


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    lo = int(a[a.index('-from') + 1]) if '-from' in a else 0
    hi = int(a[a.index('-to') + 1]) if '-to' in a else None
    odir = a[a.index('-o') + 1] if '-o' in a else None
    todo = mc14filt.gens(t, a[a.index('-g') + 1].split(','))
    print(len(todo), 'variants', flush=True)
    todo = todo[lo:hi]

    def one(it):
        name, x = it
        try:
            x0 = mc14filt.c7x(mc12vrp.threads(x))
        except Exception:
            return name, None, None, None
        if x0 is None or not 0 <= 205 - x0 <= 8:
            return name, x0, None, None
        y = mc15k.add(x, 205 - x0)
        if y is None:
            return name, 205 - x0, None, None
        return name, 205 - x0, mc1lib.score_text(y, []), y
    if odir:
        os.makedirs(odir, exist_ok=True)
    with ThreadPoolExecutor(jobs) as ex:
        for name, k, s, y in ex.map(one, todo):
            if s is None:
                print('skip', k, name, flush=True)
                continue
            d = 0 if s.get('identical') else s.get('total', 99999)
            print(d, 'k%d' % k, name, flush=True)
            if d == 0 and odir:
                open(os.path.join(odir, 'hit_%s.c' % name.replace(' ', '_')), 'w', newline='\n').write(y)


if __name__ == '__main__':
    main()
