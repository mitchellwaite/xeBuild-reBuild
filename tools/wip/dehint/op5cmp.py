"""Attempt 5: the helpers' dead cp arms as comparisons (` > 0` etc.: opcode heuristics give
75%/34%/... instead of 50%), with a neighbouring builtin removed (G/N: the expect; N: also
the entry; ib: one arm) and optionally one optricks removal.
python tools/wip/dehint/op5cmp.py FN [-r removal]"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks, op5

CMP = ['', ' > 0', ' == 1', ' < 0', ' != 1', ' == -1', ' != 0', ' < 1', ' >= 0']
TGT = ['goto r;', 'goto L6;', 'goto L5;', 'goto L1;', 'goto L3;', 'goto L4;', 'goto L2;']


def arms(allow_none=True):
    out = [None] if allow_none else []
    for c, t in itertools.product(CMP, TGT):
        out.append(c + '|' + t)
    return out


def main():
    a = sys.argv[1:]
    fn = a.pop(0)
    rem = []
    if '-r' in a:
        i = a.index('-r')
        rem = a[i + 1].split(',')
    base, got = optricks.apply(optricks.base(), rem)
    cur = op5.ntricks(fn, *op5.CUR[fn]) + len(got)
    jobs = []
    entries = [None, 'keep'] if fn == 'N' else [None]
    exps = [False, True] if fn != 'ib' else [False]
    for e, on, off, x in itertools.product(entries, arms(), arms(), exps):
        n = op5.ntricks(fn, e, on, off, x)
        if n >= op5.ntricks(fn, *op5.CUR[fn]):
            continue
        jobs.append(((e, on, off, x), n, op5.replace_fn(base, fn, op5.body(e, on, off, x))))
    print('removals', got, len(jobs), 'jobs', flush=True)
    with ThreadPoolExecutor(4) as p:
        res = list(p.map(lambda j: (j[0], j[1], optlib.score_text(j[2], optricks.flags_for(rem))), jobs))
    res.sort(key=lambda x: (x[2].get('total', 10 ** 9), x[1]))
    for k, n, r in res[:20]:
        print('%-70s n=%d %s' % (repr(k), n, optlib.fmt(r)))
    print('IDENTICAL:', [(k, n) for k, n, r in res if r.get('identical')])


if __name__ == '__main__':
    main()
