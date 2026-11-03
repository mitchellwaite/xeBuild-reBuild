"""sw.py: parallel variant runner.  run(variants, flags, tag) with variants = [(name, text)], prints sorted table of ev totals.
Importable; also: python sw.py subsets  -> all subsets of strip.ALL (with and without param 68)."""
import concurrent.futures as cf
import itertools
import sys
import threading

import mu
import strip

_loc = threading.local()
_cnt = itertools.count()


def one(v, flags, keep=False):
    name, txt = v
    if not hasattr(_loc, 'tid'):
        _loc.tid = next(_cnt)
    tag = 'w%d' % _loc.tid
    t, sc, same = mu.run_text(txt, tag, flags)
    if t is None:
        return name, 99999, str(sc)[:300], False
    return name, t, sc, same


def run(variants, flags=mu.FLAGS, top=40, quiet=False, save=None):
    """save=DIR: also write each variant to build/v/mu_d1/DIR/NAME.c for later dumps."""
    mu.ref()
    if save:
        import os
        d = os.path.join(mu.OUT, save)
        os.makedirs(d, exist_ok=True)
        for n, t in variants:
            with open(os.path.join(d, n + '.c'), 'w', newline='\n') as f:
                f.write(t)
    with cf.ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda v: one(v, flags), variants))
    res.sort(key=lambda r: r[1])
    if not quiet:
        for r in res[:top]:
            print(r[1], 'SAME' if r[3] else '', r[0], {k.lstrip('_'): v[0] for k, v in r[2].items()} if isinstance(r[2], dict) else r[2])
    return res


if __name__ == '__main__':
    if sys.argv[1] == 'subsets':
        vs = []
        for n in range(len(strip.ALL) + 1):
            for c in itertools.combinations(strip.ALL, n):
                vs.append(('-'.join(c) or 'none', strip.apply(c)))
        print('param 68')
        run(vs, '-O3 --param builtin-expect-probability=68', top=70)
