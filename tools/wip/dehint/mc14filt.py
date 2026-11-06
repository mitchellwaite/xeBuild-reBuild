"""mode_client attempt 14: mc12filt's repair families with the vrp1 block count corrected
instead of filtered.  BASE must be a k = 0 text (the help test in one `||`, no split
client_usage tests; mc14rmk.add makes the rest).  Each variant's c7 thread target x0 is
measured, k = TARGET - x0 extra blocks are added (mc14rmk.add, 0..6) and the result scored.

python tools/wip/dehint/mc14filt.py BASE.c -g less,perm,failperm,at,retarget,lists,reloc [-t 205] [-j 4] [-o DIR]"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc12filt, mc14rmk


SP = re.compile(r'__builtin_constant_p\(mode( \+ \d+)?\)')


def spell(t, n):
    """feed spellings toggled, n at a time: `mode + N` -> `mode`, `mode` -> `mode + 77`."""
    ms = list(SP.finditer(t))
    out = []
    for comb in itertools.combinations(ms, n):
        x = t
        for m in sorted(comb, key=lambda m: -m.start()):
            new = '__builtin_constant_p(mode)' if m.group(1) else '__builtin_constant_p(mode + 77)'
            x = x[:m.start()] + new + x[m.end():]
        out.append(('spell%d %s' % (n, '/'.join(str(m.start()) for m in comb)), x))
    return out


def gens(t, names):
    import mc9rep, mc10edits
    out = []
    for g in names:
        if g.startswith('lists:'):
            import mc7j2l, mc8comp
            out += [(d, mc7j2l.apply(t, ed)) for d, ed in mc8comp.edits(t) if g[6:] in d]
        elif g.startswith('spell'):
            out += spell(t, int(g[5:] or 1))
        elif g == 'at':
            out += [('at %d' % n, v) for n, (_, v) in enumerate(mc10edits.variants(t))]
        elif g == 'failperm':
            out += mc12filt.g_failperm(t)
        elif g == 'reloc':
            out += mc12filt.g_reloc(t)
        else:
            out += [('%s %d' % (g, n), x) for n, x in enumerate(mc9rep.GENS[g](t))]
    return out


def c7x(th):
    v = sorted(int(x) for _, _, x in th[:3] if x != '?')
    # a case head with one pred (c11 without its feed) has no split: its target is an
    # old block far below the new ones; skip it
    while len(v) > 1 and v[1] - v[0] > 10:
        v = v[1:]
    return v[0] if v else None


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    tgt = int(a[a.index('-t') + 1]) if '-t' in a else 205
    odir = a[a.index('-o') + 1] if '-o' in a else None
    todo = gens(t, a[a.index('-g') + 1].split(','))
    print(len(todo), 'variants', flush=True)

    def one(it):
        name, x = it
        try:
            x0 = c7x(mc12vrp.threads(x))
        except Exception:
            return name, None, None, None
        if x0 is None or not 0 <= tgt - x0 <= 6:
            return name, x0, None, None
        y = mc14rmk.add(x, tgt - x0)
        if y is None:
            return name, x0, None, None
        return name, tgt - x0, mc1lib.score_text(y, []), y
    if odir:
        os.makedirs(odir, exist_ok=True)
    best = []
    with ThreadPoolExecutor(jobs) as ex:
        for name, k, s, y in ex.map(one, todo):
            if s is None:
                continue
            d = 0 if s.get('identical') else s.get('total', 99999)
            print(d, 'k%d' % k, name, flush=True)
            if d == 0 and odir:
                open(os.path.join(odir, 'hit_%s.c' % name.replace(' ', '_').replace('@', '_')), 'w', newline='\n').write(y)


if __name__ == '__main__':
    main()
