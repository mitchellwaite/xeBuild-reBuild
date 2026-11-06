"""mode_client attempt 9 (from mc6chain): only combinations with fewer terms than
-lt N (default 10), else-chained.  Attempt 6: the mode = 7/11/9 chain before the switch with other term counts
and arm orders (an arm sends 1/2^k of what reaches it).

python tools/wip/dehint/mc6chain.py BASE.c [-j 5] [-max 6]
Prints IDENTICAL combinations (with the trick count) and the best misses."""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

RX = r'if \((?:__builtin_constant_p\(mode \+ \d+\)(?: && )?)+\) mode = \d+;(?: else if \((?:__builtin_constant_p\(mode \+ \d+\)(?: && )?)+\) mode = \d+;)*(?= switch)'


def arm(v, k):
    return 'if (%s) mode = %d;' % (' && '.join('__builtin_constant_p(mode + %d)' % (900000 + 1000 * v + j)
                                                for j in range(k)), v)


def main():
    a = sys.argv[1:]
    base = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 5
    mx = int(a[a.index('-max') + 1]) if '-max' in a else 6
    lt = int(a[a.index('-lt') + 1]) if '-lt' in a else 10
    m = re.search(RX, base)
    todo = []
    for order in itertools.permutations((7, 11, 9)):
        for ks in itertools.product(range(0, mx + 1), repeat=3):
            arms = [arm(v, k) for v, k in zip(order, ks) if k]
            if sum(ks) >= lt:
                continue
            for sep in (' else ',):
                txt = base[:m.start()] + sep.join(arms) + base[m.end():]
                todo.append(('%s %s %r' % (order, ks, sep), txt))
    todo = list(dict((t, n) for n, t in todo).items())
    todo = [(n, t) for t, n in todo]
    print(len(todo), 'variants', flush=True)

    def one(it):
        return it[0], mc1lib.score_text(it[1], []), mc1.count(it[1])['total']

    res = []
    with ThreadPoolExecutor(jobs) as ex:
        for n, s, c in ex.map(one, todo):
            if s.get('identical'):
                print('HIT', c, n, flush=True)
            elif 'total' in s:
                res.append((s['total'], c, n))
    for r in sorted(res)[:10]:
        print('  ', r)


if __name__ == '__main__':
    main()
