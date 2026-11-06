"""mode_client attempt 13: removals that cost blocks at vrp1 (mc12rm's shift < 0, plus the
extra removals below) x count-neutral repairs that may add them back (AT list adds, list
edits, ...), filtered by vrp1's thread order (mc12filt.good) before scoring.

python tools/wip/dehint/mc13neg.py BASE.c [-g rep:at,rep:lists] [-rm RX] [-j 4] [-o DIR] [-min -3]"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc12filt, mc12rm

EXTRA = [
    ('k61l', "if ((char *)__builtin_constant_p(i + 300) == (char *)1 && (char *)__builtin_constant_p(i + 300 + 1) == (char *)1) goto k61l;", ''),
    ('arm9', 'if (__builtin_constant_p(mode + 909000)) mode = 9; else ', ''),
]


def xs_of(th):
    return sorted(int(x) for _, _, x in th[:3] if x != '?')


def gen(t, g):
    out = []
    for gg in g.split(','):
        if gg.startswith('rep:'):
            import mc9rep, mc10edits
            gens = dict(mc9rep.GENS)
            gens['at'] = lambda t: [v for _, v in mc10edits.variants(t)]
            out += [('%s %d' % (gg, n), x) for n, x in enumerate(gens[gg[4:]](t))]
        else:
            out += getattr(mc12filt, 'g_' + gg)(t)
    return out


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    g = a[a.index('-g') + 1] if '-g' in a else 'rep:at'
    rx = a[a.index('-rm') + 1] if '-rm' in a else None
    mn = int(a[a.index('-min') + 1]) if '-min' in a else -2
    odir = a[a.index('-o') + 1] if '-o' in a else None
    base = xs_of(mc12vrp.threads(t))
    rms = mc12rm.variants(t) + [(k, t.replace(o, n, 1)) for k, o, n in EXTRA if o in t]
    if rx:
        rms = [r for r in rms if re.search(rx, r[0])]
    def sh1(r):
        try:
            return xs_of(mc12vrp.threads(r[1]))
        except Exception:
            return []
    with ThreadPoolExecutor(jobs) as ex:
        shs = list(ex.map(sh1, rms))
    todo = []
    for (k, x), xs in zip(rms, shs):
        sh = xs[1] - base[1] if len(xs) > 1 else 0
        if mn <= sh < 0:
            todo.append((k, sh, x))
    print(len(todo), 'removals with a block shift:', ', '.join('%s %+d' % (k[:40], s) for k, s, _ in todo), flush=True)
    best = []
    for k, sh, x in todo:
        vs = gen(x, g)

        def one(it):
            n, y = it
            try:
                th = mc12vrp.threads(y)
            except Exception:
                return n, None, y
            if not mc12filt.good(th):
                return n, None, y
            return n, mc1lib.score_text(y, []), y
        with ThreadPoolExecutor(jobs) as ex:
            res = [r for r in ex.map(one, vs) if r[1]]
        rows = sorted((0 if s.get('identical') else s.get('total', 99999), n, y) for n, s, y in res)
        print('%s (%+d): %d variants, %d good order, best %s' % (k[:60], sh, len(vs), len(rows),
              ' '.join('%d:%s' % (d, n) for d, n, _ in rows[:6])), flush=True)
        if odir:
            os.makedirs(odir, exist_ok=True)
            for d, n, y in rows[:2]:
                open(os.path.join(odir, '%d_%s_%s.c' % (d, re.sub(r'\W', '', k[:12]), re.sub(r'\W', '', n))), 'w', newline='\n').write(y)
        best += [(d, k, n) for d, n, _ in rows[:3]]
    print('overall', sorted(best)[:15], flush=True)


if __name__ == '__main__':
    main()
