"""mode_client attempt 10: one new feed to a target at every position of mode_client.

For near misses where a removal left one block short of frequency (chain-16: c7 after the
mode = 7 arm went; c3t5: c3 after its default feed went).  The new feed has -k terms
(1 by default); with a removal of r tricks it is a gain while k < r.

python tools/wip/dehint/mc10ins.py BASE.c -t c7[,p1] [-k 1] [-j 4] [-o DIR]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc7reloc


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    tg = a[a.index('-t') + 1].split(',')
    k = int(a[a.index('-k') + 1]) if '-k' in a else 1
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    todo = []
    for lab in tg:
        for p in mc7reloc.positions(t, 'mode_client'):
            cond = ' && '.join('__builtin_constant_p(mode + %d)' % (700000 + 10 * p + j) for j in range(k))
            todo.append(('%s@%d' % (lab, p), t[:p] + ' if (%s) goto %s;' % (cond, lab) + t[p:], p))
    print(len(todo), 'variants', flush=True)
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1], []), it[1], it[2]), todo))
    rows = sorted((0 if s.get('identical') else s.get('total', 99999), n, x, p) for n, s, x, p in res)
    for d, n, _, p in rows[:12]:
        print(d, n, repr(t[max(0, p - 60):p]), flush=True)
    if odir:
        os.makedirs(odir, exist_ok=True)
        for d, n, x, p in rows[:3]:
            if d == 0:
                open(os.path.join(odir, 'h_ins_%s.c' % n.replace('@', '_')), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()
