"""mode_client attempt 8: the latch flip is a free-list artifact (dce3 releases the folded
cp feeds' `mode + N` temporaries, PRE pops them).  Count-neutral toggle: change how many
temporaries one cp argument has: `cp(mode + N)` -> `cp(mode)` (one fewer) or
`cp(mode * 3 + N)` (one more).  Singles, and with -pairs all pairs of singles.

python tools/wip/dehint/mc8tmp.py BASE.c [-j 4] [-pairs] [-o DIR]"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib

RX = r'__builtin_constant_p\((mode|block|i) \+ (\d+)( \+ 1)?\)'


def sites(t):
    out = []
    for m in re.finditer(RX, t):
        v = m.group(1)
        out.append(('less@%d' % m.start(), (m.start(), m.end(), '__builtin_constant_p(%s)' % v)))
        out.append(('more@%d' % m.start(), (m.start(), m.end(), '__builtin_constant_p(%s * 3 + %s)' % (v, m.group(2)))))
    return out


def apply(t, eds):
    for s, e, x in sorted(eds, key=lambda z: -z[0]):
        t = t[:s] + x + t[e:]
    return t


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    ss = sites(t)
    todo = [(k, apply(t, [e])) for k, e in ss]
    if '-pairs' in a:
        todo += [('%s+%s' % (k1, k2), apply(t, [e1, e2])) for (k1, e1), (k2, e2) in itertools.combinations(ss, 2)
                 if e1[0] != e2[0]]
    print(a[0], mc1lib.fmt(mc1lib.score_text(t, []))[:40], len(todo), flush=True)
    res = []
    with ThreadPoolExecutor(jobs) as ex:
        for k, s, txt in ex.map(lambda it: (it[0], mc1lib.score_text(it[1], []), it[1]), todo):
            if 'compile' in s:
                continue
            if s['identical']:
                print('HIT', k, flush=True)
                if odir:
                    open(os.path.join(odir, 't8_%s.c' % re.sub(r'\W', '_', k)), 'w', newline='\n').write(txt)
            res.append((0 if s['identical'] else s['total'], k))
    res.sort()
    print('best', res[:12], flush=True)


if __name__ == '__main__':
    main()
