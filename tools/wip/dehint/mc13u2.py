"""mode_client attempt 13: one feed statement (given literally) moved to every position in
mode_client, filtered by vrp1's thread order, scored.  For the `cp(mode)` u2 feed, which
mc12filt's reloc regex (`mode + N` only) skips.

python tools/wip/dehint/mc13u2.py BASE.c [-s 'if (__builtin_constant_p(mode)) goto u2;'] [-j 4] [-o DIR]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc7reloc, mc12vrp, mc12filt


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    st = a[a.index('-s') + 1] if '-s' in a else 'if (__builtin_constant_p(mode)) goto u2;'
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    i = t.index(st, t.index('int mode_client('))
    u = t[:i] + t[i + len(st):]
    vs = [('@%d' % p, u[:p] + ' ' + st + u[p:]) for p in mc7reloc.positions(u, 'mode_client')]
    print(len(vs), 'positions', flush=True)

    def one(it):
        try:
            th = mc12vrp.threads(it[1])
        except Exception:
            return it[0], None, it[1]
        if not mc12filt.good(th):
            return it[0], None, it[1]
        return it[0], mc1lib.score_text(it[1], []), it[1]
    with ThreadPoolExecutor(jobs) as ex:
        res = [r for r in ex.map(one, vs) if r[1]]
    rows = sorted((0 if s.get('identical') else s.get('total', 99999), k, x) for k, s, x in res)
    print(len(rows), 'with the reference thread order', flush=True)
    for d, k, _ in rows[:15]:
        print(d, k, flush=True)
    if odir:
        os.makedirs(odir, exist_ok=True)
        for n, (d, k, x) in enumerate(rows[:3]):
            open(os.path.join(odir, 'u_%d_%d.c' % (n, d)), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()
