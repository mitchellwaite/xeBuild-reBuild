"""Attempt 3: the rev feeds of dz1/dz2 as nests whose levels are `cp`, `cp == 1` (opcode
heuristic, one builtin) or `__builtin_expect(cp, 0)` (two builtins); reports matches with
their builtin count.

python tools/wip/dehint/oprev3.py [dz1|dz2]"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

D1 = '\t\t\tif (__builtin_constant_p(xb.blSuffix[1] + 1)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 2), 0)) goto dz1; }\n'
D2 = '\t\t\tif (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; }\n'
LV = {'c': ('__builtin_constant_p(xb.blSuffix[1] + %d)', 1),
      'q': ('__builtin_constant_p(xb.blSuffix[1] + %d) == 1', 1),
      'e': ('__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + %d), 0)', 2)}


def nest(levels, base, lab):
    s = ''
    for k, l in enumerate(levels):
        s += 'if (%s) { ' % (LV[l][0] % (base + k))
    s = s[:-2] + 'goto %s;' % lab + ' }' * (len(levels) - 1)
    return '\t\t\t' + s + '\n'


def run(item):
    which, levels = item
    t = optlib.read_src(optlib.SRC)
    assert D1 in t and D2 in t
    if which == 'dz1':
        t = t.replace(D1, nest(levels, 1, 'dz1'))
    else:
        t = t.replace(D2, nest(levels, 15, 'dz2'))
    return which, levels, sum(LV[l][1] for l in levels), optlib.fmt(optlib.score_text(t))


if __name__ == '__main__':
    which = sys.argv[1:] or ['dz1', 'dz2']
    items = [(w, ''.join(p)) for w in which for d in (1, 2, 3) for p in itertools.product('cqe', repeat=d)]
    with ThreadPoolExecutor(6) as ex:
        for w, lv, n, r in ex.map(run, items):
            print(w, lv, n, r[:100])
