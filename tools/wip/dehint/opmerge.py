"""opmerge.py: merge applyIniOptions' identical optIniBool copies (optE/optC/optS/optU, and
optionally optN) into one, every subset of call sites redirected, scored with optlib."""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

NAMES = ['optE', 'optC', 'optS', 'optU']


def drop_def(t, n):
    i = t.index('static _Bool %s(' % n)
    j = t.index('\n}\n', i) + 3
    return t[:i] + t[j:]


def make(keep, merged):
    t = optlib.read_src(optlib.SRC)
    for n in merged:
        t = drop_def(t, n)
        t = re.sub(r'\b%s\("' % n, keep + '("', t)
    return t


if __name__ == '__main__':
    combos = []
    for keep in NAMES:
        others = [n for n in NAMES if n != keep]
        for k in range(1, 4):
            for c in itertools.combinations(others, k):
                combos.append((keep, c))

    def one(c):
        return c, optlib.score_text(make(*c))
    with ThreadPoolExecutor(6) as p:
        rs = list(p.map(one, combos))
    rs.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for (k, c), r in rs:
        print('%s <- %-20s %s' % (k, ','.join(c), optlib.fmt(r)))
