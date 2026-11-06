"""mode_client attempt 7: count-neutral relocation of every 1-term feed of mode_client on a
near-miss base (a feed moved elsewhere changes the SSA numbering and the source block's
flow; used to repair the latch-compare flip and tail swaps that near misses leave).

python tools/wip/dehint/mc7relocall.py BASE.c [-j 4] [-o DIR] [-only TARGET,...]
Stops at the first IDENTICAL hit per feed; hits -> DIR/ra_<target>_<pos>.c"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc7reloc

FEED = r' ?if \(__builtin_constant_p\((?:mode|i) \+ \d+\)\) goto (\w+);'


def main():
    a = sys.argv[1:]
    base = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    only = a[a.index('-only') + 1].split(',') if '-only' in a else None
    s0 = base.index('int mode_client(')
    feeds = [(m.start() + s0, m.end() + s0, m.group(1)) for m in re.finditer(FEED, base[s0:])]
    print(a[0], 'count', mc1.count(base)['total'], len(feeds), 'feeds', flush=True)
    for fs, fe, tgt in feeds:
        if only and tgt not in only:
            continue
        t = base[:fs] + base[fe:]
        todo = []
        for p in mc7reloc.positions(t, 'mode_client'):
            st = ' if (__builtin_constant_p(mode + %d)) goto %s;' % (600000 + 10 * p, tgt)
            todo.append((p, t[:p] + st + t[p:]))
        with ThreadPoolExecutor(jobs) as ex:
            res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1]), it[1]), todo))
        rows = []
        for p, s, txt in res:
            if 'compile' in s:
                continue
            d = 0 if s['identical'] else s['total']
            rows.append((d, abs(p - fs), p, txt))
        rows.sort(key=lambda r: r[:2])
        hits = [r for r in rows if r[0] == 0]
        print('feed', tgt, '@%d' % fs, 'hits', len(hits), 'best', [(r[0], r[2]) for r in rows[:5]], flush=True)
        for d, _, p, txt in hits[:3]:
            print('HIT', tgt, p, repr(t[max(0, p - 50):p]), flush=True)
            if odir:
                open(os.path.join(odir, 'ra_%s_%d.c' % (tgt, p)), 'w', newline='\n').write(txt)


if __name__ == '__main__':
    main()
