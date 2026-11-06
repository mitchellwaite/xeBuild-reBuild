"""mode_client attempt 6: greedy feed shortening.  For each multi-term feed (or mode-chain
arm), remove it and look for a 1-term (then 2-term, ...) feed into the same target from any
position of mode_client (mc6feedpos's positions) that keeps the object IDENTICAL; take the
hit nearest the removed feed and go on to the next one.

python tools/wip/dehint/mc6short.py BASE.c OUT.c [-j 5]
Log on stdout; the state after each accepted change is written to OUT.c."""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc6feedpos

CP = r'__builtin_constant_p\(mode \+ \d+\)'
# (name, regex of the construct to remove, target label, terms it has)
FEEDS = [
    ('t5', r'if \(__builtin_constant_p\(mode \+ 3000\)[^;]*goto t5;', 't5', 4),
    ('c11', r'if \(__builtin_constant_p\(mode \+ 2400\)[^;]*goto c11;', 'c11', 4),
    ('c3', r'if \(__builtin_constant_p\(mode \+ 205\) [^;]*goto c3;', 'c3', 4),
    ('t4', r'if \(__builtin_constant_p\(mode \+ 930\)[^;]*goto t4;', 't4', 4),
    ('s5', r'if \(__builtin_constant_p\(mode \+ 730\)[^;]*goto s5;', 's5', 4),
    ('a7', r'if \(__builtin_constant_p\(mode \+ 1210\)[^;]*mode = 7; else ', 'c7', 6),
    ('a11', r'if \(__builtin_constant_p\(mode \+ 1230\)[^;]*mode = 11; else ', 'c11', 6),
    ('a9', r'(?:else )?if \(__builtin_constant_p\(mode \+ 1221\)[^;]*mode = 9; ', 'c9', 5),
]


def search(t, tgt, k, jobs, near):
    todo = []
    for p in mc6feedpos.positions(t):
        f = ' if (%s) goto %s;' % (' && '.join('__builtin_constant_p(mode + %d)' % (800000 + 10 * p + j)
                                                 for j in range(k)), tgt)
        todo.append((p, t[:p] + f + t[p:]))
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1]), it[1]), todo))
    hits = [(abs(p - near), p, txt) for p, s, txt in res if s.get('identical')]
    best = min((s['total'], p) for p, s, _ in res if 'total' in s and not s.get('identical')) if res else None
    return sorted(hits), best


def main():
    a = sys.argv[1:]
    base, out = a[0], a[1]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 5
    only = a[a.index('-only') + 1].split(',') if '-only' in a else None
    cur = mc1lib.read_src(base)
    print('base', mc1.count(cur)['total'], mc1lib.fmt(mc1lib.score_text(cur)), flush=True)
    feeds = FEEDS
    if '-auto' in a:
        # every goto feed of mode_client with 2 or more terms (pass 2: the names above
        # no longer match the relocated feeds)
        s = cur.index('int mode_client(')
        feeds = []
        for m in re.finditer(r'if \(((?:__builtin_constant_p\(mode \+ \d+\)(?: && )?)+)\) goto (\w+);', cur[s:]):
            n = m.group(1).count('__builtin_constant_p')
            if n >= 2:
                feeds.append(('%s/%d' % (m.group(2), n), re.escape(m.group(0)), m.group(2), n))
    for name, rx, tgt, n in feeds:
        if only and name not in only:
            continue
        m = re.search(rx, cur)
        if not m:
            print(name, 'not found', flush=True)
            continue
        t = cur[:m.start()] + cur[m.end():]
        for k in range(1, n):
            hits, best = search(t, tgt, k, jobs, m.start())
            print(name, 'k', k, 'hits', len(hits), 'best miss', best, flush=True)
            if hits:
                d, p, txt = hits[0]
                cur = txt
                open(out, 'w', newline='\n').write(cur)
                print('took', name, 'k', k, '@', p, repr(cur[max(0, p - 40):p + 70]),
                      'count', mc1.count(cur)['total'], flush=True)
                break
    print('final', mc1.count(cur)['total'], mc1lib.fmt(mc1lib.score_text(cur)), flush=True)


if __name__ == '__main__':
    main()
