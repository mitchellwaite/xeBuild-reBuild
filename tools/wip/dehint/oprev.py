"""oprev.py: cheaper feeds for the dz1/dz2 dummies (the rev block's dead __builtin_constant_p
arms), every pair of forms, on src/options.c, scored with optlib."""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

CP = '__builtin_constant_p(xb.blSuffix[1] + %d)'
EX0 = '__builtin_expect(' + CP + ', 0)'
EX1 = '__builtin_expect(' + CP + ', 1)'


def nest(conds, lab):
    """nested ifs of the given condition templates, numbered from a base"""
    s = 'goto %s;' % lab
    for c in reversed(conds):
        s = 'if (%s) { %s }' % (c, s)
    return s


FORMS = {
    'c': [CP], 'e0': [EX0], 'e1': [EX1],
    'cc': [CP, CP], 'e0c': [EX0, CP], 'ce1': [CP, EX1], 'e0e1': [EX0, EX1],
    'ccc': [CP, CP, CP], 'e0cc': [EX0, CP, CP], 'e0ce1': [EX0, CP, EX1],
    'cccc': [CP] * 4, 'e0ccc': [EX0, CP, CP, CP], 'e0ccce1': [EX0, CP, CP, CP, EX1],
    'e0cce1': [EX0, CP, CP, EX1], 'ccce1': [CP, CP, CP, EX1], 'e0e0': [EX0, EX0],
    'e1e0': [EX1, EX0], 'e0e0e0': [EX0, EX0, EX0], 'e0e0c': [EX0, EX0, CP], 'e0e0e1': [EX0, EX0, EX1],
    'e0e1e1': [EX0, EX1, EX1], 'e1e1': [EX1, EX1], 'e1c': [EX1, CP], 'ce0': [CP, EX0], 'cce1': [CP, CP, EX1],
    'e1e1e0': [EX1, EX1, EX0], 'e1e0e0': [EX1, EX0, EX0], 'ce0e0': [CP, EX0, EX0],
}


def render(form, lab, base):
    cs = [c % (base + i) for i, c in enumerate(FORMS[form])]
    return '\t\t\t' + nest(cs, lab) + '\n'


L1 = re.compile(r'\t\t\tif \(__builtin_expect\(__builtin_constant_p\(xb\.blSuffix\[1\] \+ 1\), 0\)\).*goto dz1;.*\n')
L2 = re.compile(r'\t\t\tif \(__builtin_expect\(__builtin_constant_p\(xb\.blSuffix\[1\] \+ 15\), 0\)\).*goto dz2;.*\n')


def make(f1, f2):
    t = optlib.read_src(optlib.SRC)
    assert L1.search(t) and L2.search(t)
    t = L1.sub(lambda m: render(f1, 'dz1', 1), t)
    t = L2.sub(lambda m: render(f2, 'dz2', 15), t)
    return t


if __name__ == '__main__':
    a = sys.argv[1:]
    f1s = a[0].split(',') if a else list(FORMS)
    f2s = a[1].split(',') if len(a) > 1 else ['e0ccce1']

    def one(c):
        return c, optlib.score_text(make(*c))
    with ThreadPoolExecutor(6) as p:
        for c, r in p.map(one, itertools.product(f1s, f2s)):
            print('%-8s %-8s %s' % (c[0], c[1], optlib.fmt(r)), flush=True)
