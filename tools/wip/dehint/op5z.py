"""Attempt 5: parseButtonX's z feed (3 cp now) as 1-2 tests whose conditions are cp
compared with constants (opcode heuristics give other probabilities than 50%) or
expect(cp, 0|1).  python tools/wip/dehint/op5z.py"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks, op5bx

C = ['cp', 'cp == 1', 'cp != 1', 'cp > 0', 'cp < 0', 'cp >= 1', 'cp <= 0', 'cp != 0', 'cp == 0',
     'cp > 1', 'cp == -1', 'cp != -1', 'cp < 1', '!cp', '__builtin_expect(cp, 0)', '__builtin_expect(cp, 1)']


def cond(c, k):
    return c.replace('cp', '__builtin_constant_p(xb.xellButton + %d)' % k).replace('__builtin_expect(__builtin_constant_p', '__builtin_expect(__builtin_constant_p')


def nb(c):
    return 1 + ('expect' in c)


def main():
    b = optricks.base()
    jobs = []
    for a in C:
        jobs.append(('1[%s]' % a, nb(a), 'if (%s) goto z;' % cond(a, 1)))
    for a, c in itertools.product(C, C):
        if nb(a) + nb(c) > 2:
            continue
        jobs.append(('n[%s|%s]' % (a, c), 2, 'if (%s) { if (%s) goto z; }' % (cond(a, 1), cond(c, 2))))
        jobs.append(('o[%s|%s]' % (a, c), 2, 'if (%s) goto z; if (%s) goto z;' % (cond(a, 1), cond(c, 2))))
    with ThreadPoolExecutor(4) as p:
        res = list(p.map(lambda j: (j[0], j[1], optlib.score_text(op5bx.replace_fn(b, op5bx.body(0, j[2], True)))), jobs))
    res.sort(key=lambda x: (x[2].get('total', 10 ** 9), x[1]))
    for k, n, r in res[:25]:
        print('%-60s n=%d %s' % (k, n, optlib.fmt(r)))
    print('IDENTICAL:', [(k, n) for k, n, r in res if r.get('identical')])


if __name__ == '__main__':
    main()
