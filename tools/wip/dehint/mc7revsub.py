"""mode_client attempt 7: every subset of the arms whose `x = argv[i + 1]; i++;` is written
`x = argv[++i];` (attempt 3's spelling and its revert), on pure latch-flip near misses.

python tools/wip/dehint/mc7revsub.py BASE.c [BASE2.c ...] [-j 4] [-o DIR]"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc7rev


def main():
    a = sys.argv[1:]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    for b in [x for x in a if x.endswith('.c')]:
        t = mc1lib.read_src(b)
        ms = list(mc7rev.PAT.finditer(t))
        todo = []
        for k in range(1, len(ms) + 1):
            for sub in itertools.combinations(range(len(ms)), k):
                x = t
                for i in sorted(sub, reverse=True):
                    m = ms[i]
                    x = x[:m.start()] + '%s = argv[++i];' % m.group(1) + x[m.end():]
                todo.append((sub, x))
        with ThreadPoolExecutor(jobs) as ex:
            res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1]), it[1]), todo))
        rows = []
        for sub, s, x in res:
            if 'compile' in s:
                continue
            d = 0 if s['identical'] else s['total']
            if d == 0:
                print('HIT', b, sub, mc1.count(x)['total'], flush=True)
                if odir:
                    open(os.path.join(odir, 'rs_%s_%s.c' % (os.path.basename(b)[:-2], ''.join(map(str, sub)))), 'w', newline='\n').write(x)
            rows.append((d, sub))
        rows.sort()
        print(b, len(todo), 'best', rows[:8], flush=True)


if __name__ == '__main__':
    main()
