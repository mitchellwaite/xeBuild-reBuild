"""mode_client attempt 12: count-neutral micro-variants filtered by vrp1's thread order.

The reference threads the mode-chain switch as arm 11, arm 7, arm 9 (sources sorted by
index: mid, last, first).  Variants are generated, their vrp1 order checked (mc12vrp), and
only those with the reference order are compiled and scored.

python tools/wip/dehint/mc12filt.py BASE.c -g cebifeed,dyblock,failperm,reloc[:TARGET] [-j 4] [-o DIR] [-all]"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc7reloc, mc12vrp

CEBI_FEED = re.compile(r' ?if \(__builtin_constant_p\(block[^)]*\)\) goto dy;')
DY = re.compile(r'if \(0\) \{ dy: __builtin_unreachable\(\); \} ?')
FEED = re.compile(r' ?if \(__builtin_constant_p\((?:mode|i) \+ \d+\)\) goto (\w+);')


def g_cebifeed(t):
    m = CEBI_FEED.search(t)
    st = m.group(0).strip()
    u = t[:m.start()] + t[m.end():]
    return [('cebifeed@%d' % p, u[:p] + ' ' + st + u[p:]) for p in mc7reloc.positions(u, 'clientEraseBlockI')]


def g_dyblock(t):
    m = DY.search(t)
    st = m.group(0).strip()
    u = t[:m.start()] + t[m.end():]
    return [('dy@%d' % p, u[:p] + ' ' + st + ' ' + u[p:]) for p in mc7reloc.positions(u, 'clientEraseBlockI')]


def g_failperm(t):
    k = t.index('fail: __attribute__((cold));')
    e = t.index('return 0;\n}', k)
    seg = t[k + len('fail: __attribute__((cold));'):e]
    lg = re.search(r'log_printf\(0, "[^"]*unable to connect[^"]*"\);', seg).group(0)
    feeds = [m.group(0).strip() for m in FEED.finditer(seg)]
    items = feeds + [lg]
    out = []
    for p in itertools.permutations(items):
        s = ' ' + '\n\t'.join(p) + '\n\t'
        out.append(('perm ' + '|'.join(x.split('goto ')[-1][:-1] if 'goto' in x else 'LOG' for x in p),
                    t[:k + len('fail: __attribute__((cold));')] + s + t[e:]))
    return out


def g_reloc(t, only=None):
    s0 = t.index('int mode_client(')
    out = []
    for m in FEED.finditer(t, s0):
        if only and m.group(1) not in only:
            continue
        st = m.group(0).strip()
        u = t[:m.start()] + t[m.end():]
        for p in mc7reloc.positions(u, 'mode_client'):
            out.append(('reloc %s@%d' % (m.group(1), p), u[:p] + ' ' + st + u[p:]))
    return out


def good(th):
    xs = [(int(a), x) for a, b, x in th if b == th[0][1]]
    if len(xs) != 3:
        return False
    srt = sorted(a for a, _ in xs)
    return [a for a, _ in xs] == [srt[1], srt[2], srt[0]]


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    todo = []
    for g in a[a.index('-g') + 1].split(','):
        if g.startswith('reloc'):
            todo += g_reloc(t, g.split(':')[1].split('+') if ':' in g else None)
        elif g.startswith('rep:'):
            import mc9rep, mc10edits
            gens = dict(mc9rep.GENS)
            gens['at'] = lambda t: [v for _, v in mc10edits.variants(t)]
            todo += [('%s %d' % (g, n), x) for n, x in enumerate(gens[g[4:]](t))]
        else:
            todo += globals()['g_' + g](t)
    print(len(todo), 'variants', flush=True)

    def one(it):
        k, x = it
        try:
            th = mc12vrp.threads(x)
        except Exception as ex:
            return k, None, 'err', x
        if not good(th) and '-all' not in a:
            return k, th, None, x
        return k, th, mc1lib.score_text(x, []), x
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(one, todo))
    ok = [r for r in res if r[2] and r[2] != 'err']
    print(len(ok), 'with the reference thread order', flush=True)
    rows = sorted((0 if s.get('identical') else s.get('total', 99999), k, x) for k, th, s, x in ok)
    for d, k, _ in rows[:20]:
        print(d, k, flush=True)
    if odir:
        os.makedirs(odir, exist_ok=True)
        for n, (d, k, x) in enumerate(rows[:3]):
            open(os.path.join(odir, 'f_%d_%d.c' % (n, d)), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()
