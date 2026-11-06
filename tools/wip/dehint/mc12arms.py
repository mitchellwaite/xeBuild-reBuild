"""mode_client attempt 12: redistribute the mode-chain arm terms (mode = 9 / 11 / 7) between
the arms, total count kept (or -d N: N terms fewer in total).  More terms in an arm make
its case head colder (each && halves the share), so moving a term from arm 11 to arm 7 warms
c11 and cools c7 at once.

python tools/wip/dehint/mc12arms.py BASE.c [-d 0] [-j 4] [-o DIR] [-min 1]"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib

RX = re.compile(r'if \((__builtin_constant_p\(mode \+ 909\d+\)(?: && __builtin_constant_p\(mode \+ 909\d+\))*)\) mode = 9; '
                r'else if \((__builtin_constant_p\(mode \+ 911\d+\)(?: && __builtin_constant_p\(mode \+ 911\d+\))*)\) mode = 11; '
                r'else if \((__builtin_constant_p\(mode \+ 907\d+\)(?: && __builtin_constant_p\(mode \+ 907\d+\))*)\) mode = 7;')


def arm(base, n, off=0):
    return ' && '.join('__builtin_constant_p(mode + %d)' % (base + off + k) for k in range(n))


def build(t, a, b, c, off=0):
    m = RX.search(t)
    s = ('if (%s) mode = 9; else if (%s) mode = 11; else if (%s) mode = 7;'
         % (arm(909000, a, off), arm(911000, b, off), arm(907000, c, off)))
    return t[:m.start()] + s + t[m.end():]


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    d = int(a[a.index('-d') + 1]) if '-d' in a else 0
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    mn = int(a[a.index('-min') + 1]) if '-min' in a else 1
    odir = a[a.index('-o') + 1] if '-o' in a else None
    m = RX.search(t)
    cur = [g.count('__builtin_constant_p') for g in m.groups()]
    tot = sum(cur) - d
    print('current', cur, 'total', tot, flush=True)
    todo = []
    for x in range(mn, tot + 1):
        for y in range(mn, tot - x + 1):
            z = tot - x - y
            if z < mn:
                continue
            todo.append(('arms %d/%d/%d' % (x, y, z), build(t, x, y, z)))
    print(len(todo), 'variants', flush=True)
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1], []), it[1]), todo))
    rows = sorted((0 if s.get('identical') else s.get('total', 99999), k, x) for k, s, x in res)
    for dd, k, _ in rows[:15]:
        print(dd, k, flush=True)
    if odir:
        os.makedirs(odir, exist_ok=True)
        for n, (dd, k, x) in enumerate(rows[:3]):
            if dd == 0:
                open(os.path.join(odir, 'h_arms_%d.c' % n), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()
