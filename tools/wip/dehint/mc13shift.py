"""mode_client attempt 13: block-count shift at vrp1 of source edits, relative to a base.

The shift is the c7 thread target's index minus the base's (mc12vrp's x).  Edits are
(name, old, new) triples applied once each to the base; prints the shift and the thread
order (GOOD = the reference's arm 11, 7, 9).

python tools/wip/dehint/mc13shift.py BASE.c EDITS.py [-j 4] [-score]
EDITS.py defines EDITS = [(name, old, new), ...] (old must occur in BASE; first one replaced)."""
import os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc12filt


def x_of(th):
    xs = sorted(int(x) for _, _, x in th[:3] if x != '?')
    return xs


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    g = {}
    exec(open(a[1]).read(), g)
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    base = x_of(mc12vrp.threads(t))
    print('base', base, flush=True)

    def one(e):
        name, old, new = e
        if old not in t:
            return name, None, 'missing', None
        x = t.replace(old, new, 1)
        try:
            th = mc12vrp.threads(x)
        except Exception:
            return name, None, 'err', None
        s = mc1lib.score_text(x, []) if '-score' in a else None
        return name, th, x_of(th), s
    with ThreadPoolExecutor(jobs) as ex:
        for name, th, xs, s in ex.map(one, g['EDITS']):
            if th is None:
                print(name, xs, flush=True)
                continue
            sh = xs[1] - base[1] if len(xs) > 1 and len(base) > 1 else '?'
            sc = '' if s is None else (0 if s.get('identical') else s.get('total'))
            print('%+s' % sh, 'GOOD' if mc12filt.good(th) else 'bad ', xs, sc, name, flush=True)


if __name__ == '__main__':
    main()
