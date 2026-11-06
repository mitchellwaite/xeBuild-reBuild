"""mode_client attempt 6: drop a dead block with its asm goto edge (JMP(dz) / dz, or dv from
rok's list) and replace the edge by a 1- or 2-term cp feed from a window of positions to any
label of mode_client.

python tools/wip/dehint/mc6dead.py BASE.c dz|dv [-j 5] [-w CHARS]
Prints IDENTICAL hits with the count, then the best misses."""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc6feedpos, mc6walk


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    which = a[1]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 5
    w = int(a[a.index('-w') + 1]) if '-w' in a else 400
    if which == 'dz':
        anchor = t.index(' JMP(dz);')
        t = t.replace(' JMP(dz);', '', 1)
        t = t.replace('if (0) { dz: __builtin_unreachable(); }', '', 1)
    else:
        m = re.search(r'__asm__ goto \("" :::: dv, ', t)
        anchor = m.start()
        t = t[:m.start()] + '__asm__ goto ("" :::: ' + t[m.end():]
        t = t.replace('if (0) { dv: __builtin_unreachable(); }', '', 1)
    print('removed', which, 'count', mc1.count(t)['total'], mc1lib.fmt(mc1lib.score_text(t)), flush=True)
    labs = sorted(mc6walk.defined(t) - {'default'})
    s = t.index('int mode_client(')
    labs = [l for l in labs if not re.match(r'(o?fa|rk|ork|rkn)\d', l)]
    todo = []
    for p in mc6feedpos.positions(t):
        if abs(p - anchor) > w:
            continue
        for L in labs:
            for k in (1, 2):
                f = ' if (%s) goto %s;' % (' && '.join('__builtin_constant_p(i + %d)' % (970000 + j) for j in range(k)), L)
                todo.append(('@%d %s k%d' % (p - anchor, L, k), t[:p] + f + t[p:]))
    print(len(todo), 'variants', flush=True)

    def one(it):
        return it[0], mc1lib.score_text(it[1]), mc1.count(it[1])['total']

    res = []
    with ThreadPoolExecutor(jobs) as ex:
        for n, sc, c in ex.map(one, todo):
            if sc.get('identical'):
                print('HIT', c, n, flush=True)
            elif 'total' in sc:
                res.append((sc['total'], c, n))
    for r in sorted(res)[:12]:
        print('  ', r)


if __name__ == '__main__':
    main()
