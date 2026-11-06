"""mode_client attempt 6: replace a cp feed by its target label added to an existing asm goto
list (lists are counted per statement, so the feed's terms go and the count drops).

python tools/wip/dehint/mc6f2l.py BASE.c OUT.c [-j 5]
Greedy over the feeds of mode_client; takes the first IDENTICAL replacement of each."""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc6walk

FEED = r' ?if \(((?:__builtin_constant_p\(mode \+ \d+\)(?: && )?)+)\) goto (\w+);'


def main():
    a = sys.argv[1:]
    cur = mc1lib.read_src(a[0])
    out = a[1]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 5
    print('base', mc1.count(cur)['total'], flush=True)
    s0 = cur.index('int mode_client(')
    feeds = [m.group(0) for m in re.finditer(FEED, cur[s0:])]
    for f in feeds:
        if cur.count(f) != 1:
            continue
        tgt = re.search(r'goto (\w+);', f).group(1)
        t = cur.replace(f, '', 1)
        todo = []
        for k, (p, q, s) in enumerate(mc6walk.lists(t)):
            items = [x.strip() for x in s.split(',')]
            if tgt in items:
                continue
            sep = ', ' if ', ' in s else ','
            todo.append((k, t[:p] + sep.join(items + [tgt]) + t[q:]))
        todo.append((-1, t))
        with ThreadPoolExecutor(jobs) as ex:
            res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1]), it[1]), todo))
        hits = [(k, txt) for k, s, txt in res if s.get('identical')]
        best = sorted((s.get('total', 99999), k) for k, s, _ in res)[:3]
        print('%-60s hits %s best %s' % (f[:60], [k for k, _ in hits], best), flush=True)
        if hits:
            cur = hits[0][1]
            open(out, 'w', newline='\n').write(cur)
            print('took', hits[0][0], 'count', mc1.count(cur)['total'], flush=True)
    print('final', mc1.count(cur)['total'], mc1lib.fmt(mc1lib.score_text(cur)), flush=True)


if __name__ == '__main__':
    main()
