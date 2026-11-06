"""Attempt 3: `__builtin_expect(__builtin_constant_p(X), 0|1)` feeds respelled as a comparison of
the cp result that folds to false (cp ends up 0) but carries an opcode heuristic instead of the
expect: one trick instead of two per feed.  Each site alone, then all sites that match.

python tools/wip/dehint/opcmp.py"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

PAT = re.compile(r'__builtin_expect\((__builtin_constant_p\([^()]*\)), ([01])\)')
FORMS = {'0': ['%s == 1', '%s == 2', '%s < 0', '%s <= -1', '%s > 1', '%s >= 2', '%s == -1'],
         '1': ['%s >= 1', '%s > 0', '%s >= 2', '%s > 1', '%s != 0']}


def sites(t):
    return [m for m in PAT.finditer(t)]


def sub(t, picks):
    """picks: {site index: form}"""
    ms = sites(t)
    out, last = [], 0
    for i, m in enumerate(ms):
        out.append(t[last:m.start()])
        out.append(picks[i] % m.group(1) if i in picks else m.group(0))
        last = m.end()
    out.append(t[last:])
    return ''.join(out)


def run(item):
    n, picks = item
    t = sub(optlib.read_src(optlib.SRC), picks)
    return n, optlib.fmt(optlib.score_text(t))


if __name__ == '__main__':
    t = optlib.read_src(optlib.SRC)
    ms = sites(t)
    items = []
    for i, m in enumerate(ms):
        for f in FORMS[m.group(2)]:
            items.append(('s%d[%s] %s' % (i, m.group(2), f % 'cp'), {i: f}))
    hits = {}
    with ThreadPoolExecutor(6) as ex:
        for (n, r), (_, p) in zip(ex.map(run, items), items):
            print(n, r[:120], flush=True)
            if r.startswith('IDENTICAL'):
                hits.setdefault(list(p)[0], []).append(list(p.values())[0])
    print('hits', hits)
    if len(hits) > 1:
        combo = {i: v[0] for i, v in hits.items()}
        print('all hits', run(('all', combo))[1])
