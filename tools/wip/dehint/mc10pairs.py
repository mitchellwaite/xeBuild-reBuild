"""mode_client attempt 10: pairs of asm goto list edits restricted to some labels.

Every single edit (mc8comp.edits: add a label at either end of a list, drop one) whose
label is in -labs, then every compatible pair of those.  Count-neutral (list labels are
not counted).  For near misses that need a block's frequency raised by a list edge.

python tools/wip/dehint/mc10pairs.py BASE.c -labs c3,rk10,ork10 [-j 4] [-o DIR] [-singles]"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc7j2l, mc8comp


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    labs = set(a[a.index('-labs') + 1].split(','))
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    eds = [(k, ed) for k, ed in mc8comp.edits(t) if re.split(r'[ >@]', k)[1] in labs]
    todo = [(k, mc7j2l.apply(t, ed)) for k, ed in eds]
    if '-singles' not in a:
        for (k1, e1), (k2, e2) in itertools.combinations(eds, 2):
            if mc8comp.compatible(e1, e2):
                todo.append((k1 + ' + ' + k2, mc7j2l.apply(t, e1 + e2)))
    print(len(eds), 'edits', len(todo), 'variants', flush=True)
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1], []), it[1]), todo))
    rows = sorted((0 if s.get('identical') else s.get('total', 99999), k, x) for k, s, x in res)
    for d, k, _ in rows[:15]:
        print(d, k, flush=True)
    if odir:
        os.makedirs(odir, exist_ok=True)
        for n, (d, k, x) in enumerate(rows[:3]):
            if d == 0:
                open(os.path.join(odir, 'h_pair_%d.c' % n), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()
