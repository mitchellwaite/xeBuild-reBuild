"""mode_client attempt 12: count-neutral edits aimed at clientEraseBlockI only: the two
JMP(efail) lists (labels from efail, dy, einv, ybk, efc), the cebi feed's spelling and its
target.  Base must have the n49 shape of the function (`if (__builtin_constant_p(block)) goto dy;`).

python tools/wip/dehint/mc12cebi.py BASE.c [-j 4] [-o DIR] [-sp block,block + 1] [-tg dy,einv]"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib

LISTS = [['efail'], ['efail', 'dy'], ['dy', 'efail'], ['efail', 'einv'], ['einv', 'efail'],
         ['efail', 'ybk'], ['ybk', 'efail'], ['efail', 'efc']]


def variants(t, sps, tgs):
    k = t.index('static void clientEraseBlockI(')
    e = t.index('\n}\n', k)
    f = t[k:e]
    m = re.search(r'if \(__builtin_constant_p\((block[^)]*)\)\) goto (\w+);', f)
    assert m, 'no cebi feed'
    j = [x.start() for x in re.finditer(r'JMP\(efail\)', f)]
    assert len(j) == 2
    out = []
    for la, lb, sp, tg in itertools.product(LISTS, LISTS, sps, tgs):
        g = f[:m.start()] + 'if (__builtin_constant_p(%s)) goto %s;' % (sp, tg) + f[m.end():]
        # positions shift only after the feed; JMPs: first before feed, second after
        j = [x.start() for x in re.finditer(r'JMP\(efail\)', g)]
        g = (g[:j[0]] + 'JMP(%s)' % ', '.join(la) + g[j[0] + 10:j[1]] + 'JMP(%s)' % ', '.join(lb) + g[j[1] + 10:])
        key = 'A=%s B=%s sp=%s tg=%s' % ('/'.join(la), '/'.join(lb), sp, tg)
        out.append((key, t[:k] + g + t[e:]))
    return out


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    sps = a[a.index('-sp') + 1].split(',') if '-sp' in a else ['block', 'block + 1', 'block + 901']
    tgs = a[a.index('-tg') + 1].split(',') if '-tg' in a else ['dy', 'einv', 'efail']
    todo = variants(t, sps, tgs)
    print(len(todo), 'variants', flush=True)
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1], []), it[1]), todo))
    rows = sorted((0 if s.get('identical') else s.get('total', 99999), k, x) for k, s, x in res)
    for d, k, _ in rows[:15]:
        print(d, k, flush=True)
    if odir:
        os.makedirs(odir, exist_ok=True)
        for n, (d, k, x) in enumerate(rows[:3]):
            open(os.path.join(odir, 'cebi_%d_%d.c' % (n, d)), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()
