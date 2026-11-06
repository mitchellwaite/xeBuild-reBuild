"""mode_client attempt 11: asm goto list substitutions (one label replaced by another, list
length unchanged, so the other labels keep their share).  mc8comp's single edits only add
or drop; a substitution is a drop+add pair at the same slot.

python tools/wip/dehint/mc11sub.py BASE.c -t c11[,L2] [-j 4] [-o DIR]"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc7j2l


def variants(t, tg):
    out = []
    for j, o in enumerate(mc7j2l.stmts(t)):
        labs = o[5]
        for k, lab in enumerate(labs):
            for new in tg:
                if new in labs:
                    continue
                rest = labs[:k] + [new] + labs[k + 1:]
                out.append(('sub %s->%s@%d' % (lab, new, j), t[:o[3]] + ', '.join(rest) + t[o[4]:]))
    return out


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    tg = a[a.index('-t') + 1].split(',')
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    todo = variants(t, tg)
    print(len(todo), 'variants', flush=True)
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1], []), it[1]), todo))
    rows = sorted((0 if s.get('identical') else s.get('total', 99999), k, x) for k, s, x in res)
    for d, k, x in rows[:12]:
        print(d, k, flush=True)
    if odir:
        os.makedirs(odir, exist_ok=True)
        for d, k, x in rows[:3]:
            if d == 0:
                open(os.path.join(odir, 'sub_%s.c' % re.sub(r'\W+', '_', k)), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()
