"""mode_client attempt 13: block-count shift at vrp1 of every count-neutral repair edit
(mc10edits AT list adds, mc9rep lists/retarget/...), to find the edits that add blocks.

python tools/wip/dehint/mc13atsh.py BASE.c [-g at,lists] [-j 4]"""
import os, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc12filt, mc9rep, mc10edits


def xs_of(th):
    return sorted(int(x) for _, _, x in th[:3] if x != '?')


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    gs = (a[a.index('-g') + 1] if '-g' in a else 'at').split(',')
    base = xs_of(mc12vrp.threads(t))
    vs = []
    for g in gs:
        if g == 'at':
            vs += [('at ' + k, v) for k, v in mc10edits.variants(t)]
        else:
            vs += [('%s %d' % (g, n), v) for n, v in enumerate(mc9rep.GENS[g](t))]

    def one(it):
        try:
            return it[0], xs_of(mc12vrp.threads(it[1]))
        except Exception:
            return it[0], []
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(one, vs))
    c = Counter()
    for k, xs in res:
        sh = xs[1] - base[1] if len(xs) > 1 else None
        c[sh] += 1
        if sh:
            print('%+d' % sh, xs, k, flush=True)
    print('shift counts', dict(c), flush=True)


if __name__ == '__main__':
    main()
