"""mode_client attempt 8: for each removal, the removal alone + every single and pair of
`less` toggles (mc8tmp: cp(VAR + N) -> cp(VAR), count-neutral, one temporary fewer for
dce3 to release before PRE).  Writes hits to OUTDIR/l8_<name>_<key>.c.

python tools/wip/dehint/mc8less.py BASE.c OUTDIR NAME[,NAME...] [-j 4] [-k 2]"""
import itertools, os, re, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc8comp, mc8tmp


def main():
    a = sys.argv[1:]
    base = mc1lib.read_src(a[0])
    odir = a[1]
    os.makedirs(odir, exist_ok=True)
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    kmax = int(a[a.index('-k') + 1]) if '-k' in a else 2
    for name in a[2].split(','):
        t = base if name == 'none' else mc8comp.remove(base, name)
        if t is None:
            print(name, 'n/a', flush=True)
            continue
        ss = [x for x in mc8tmp.sites(t) if x[0].startswith('less')]
        todo = []
        for k in range(1, kmax + 1):
            for comb in itertools.combinations(ss, k):
                todo.append(('+'.join(c[0] for c in comb), [c[1] for c in comb]))
        res = []
        with ThreadPoolExecutor(jobs) as ex:
            for key, s, txt in ex.map(lambda kv: (kv[0], mc1lib.score_text(mc8tmp.apply(t, kv[1]), []),
                                                  mc8tmp.apply(t, kv[1])), todo):
                if 'compile' in s:
                    continue
                d = 0 if s['identical'] else s['total']
                res.append((d, key))
                if d == 0:
                    print('HIT', name, key, 'count', mc1.count(txt)['total'], flush=True)
                    open(os.path.join(odir, 'l8_%s_%s.c' % (name, re.sub(r'\W', '_', key))), 'w', newline='\n').write(txt)
                elif d <= 6:
                    open(os.path.join(odir, 'n8_%s_%d_%s.c' % (name, d, re.sub(r'\W', '_', key))), 'w', newline='\n').write(txt)
        res.sort()
        print(name, Counter(r[0] for r in res).most_common(6), 'best', res[:4], flush=True)


if __name__ == '__main__':
    main()
