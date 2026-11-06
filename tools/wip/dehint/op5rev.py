"""Attempt 5: the rev feeds of dz1/dz2 as 1-2 level nests whose conditions come from
op5z's menu (cp compared with constants: opcode heuristics) - fewer builtins wanted.
python tools/wip/dehint/op5rev.py dz1|dz2"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks, op5z

D1 = '			if (__builtin_constant_p(xb.blSuffix[1] + 1)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 2), 0)) goto dz1; return; }\n'
D2 = '			if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; }\n'
C = op5z.C + ['cp > 0', 'cp < 2', 'cp >= 0', 'cp <= -1', '__builtin_expect(cp == 1, 0)', '__builtin_expect(cp < 0, 0)']
C = list(dict.fromkeys(C))


def cond(c, k):
    return c.replace('cp', '__builtin_constant_p(xb.blSuffix[1] + %d)' % k)


def nb(c):
    return 1 + ('expect' in c)


def main():
    w = sys.argv[1]
    b = optricks.base()
    assert D1 in b and D2 in b
    jobs = []
    if w == 'dz1':
        cur = 3
        for a in C:
            if nb(a) < cur:
                jobs.append(('1[%s]' % a, nb(a), D1, '\t\t\tif (%s) { goto dz1; return; }\n' % cond(a, 1)))
        for a, c in itertools.product(C, C):
            if nb(a) + nb(c) < cur:
                jobs.append(('n[%s|%s]' % (a, c), nb(a) + nb(c), D1,
                             '\t\t\tif (%s) { if (%s) goto dz1; return; }\n' % (cond(a, 1), cond(c, 2))))
    else:
        cur = 4
        for a in C:
            jobs.append(('1[%s]' % a, nb(a), D2, '\t\t\tif (%s) goto dz2;\n' % cond(a, 15)))
        for a, c in itertools.product(C, C):
            if nb(a) + nb(c) < cur:
                jobs.append(('n[%s|%s]' % (a, c), nb(a) + nb(c), D2,
                             '\t\t\tif (%s) { if (%s) goto dz2; }\n' % (cond(a, 15), cond(c, 16))))
    with ThreadPoolExecutor(4) as p:
        res = list(p.map(lambda j: (j[0], j[1], optlib.score_text(b.replace(j[2], j[3]))), jobs))
    res.sort(key=lambda x: (x[2].get('total', 10 ** 9), x[1]))
    print(len(jobs), 'jobs')
    for k, n, r in res[:20]:
        print('%-70s n=%d %s' % (k, n, optlib.fmt(r)))
    print('IDENTICAL:', [(k, n) for k, n, r in res if r.get('identical')])


if __name__ == '__main__':
    main()
