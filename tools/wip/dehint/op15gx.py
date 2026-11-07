"""Attempt 15: optIniBoolG's whole-body shapes (op7w.py: tops x lowers x tails, most of them
IDENTICAL on the base) on top of a removal: a shape that is the same code but leaves other
stale counts could do the removed feed's job.

python tools/wip/dehint/op15gx.py [-rm rv2,..] [-site s=f,..]"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op7w


def load_site2():
    p =os.path.join(os.path.dirname(os.path.abspath(__file__)), 'op15site2.py')
    src = open(p).read().replace('\nmain()\n', '\n')
    g = {'__file__': p, '__name__': 'op15site2'}
    exec(compile(src, p, 'exec'), g)
    return g


S2 = load_site2()


def main():
    a = sys.argv[1:]
    rms = a[a.index('-rm') + 1].split(',') if '-rm' in a else []
    base = S2['apply_rm'](open(optlib.SRC).read(), rms)
    if '-site' in a:
        base = S2['assign'](base, S2['kv'](a[a.index('-site') + 1]))
    jobs = [(k, op7w.make(base, k)) for k in itertools.product(op7w.TOP, op7w.LOW, op7w.TAIL)]
    with ThreadPoolExecutor(4) as p:
        res = list(p.map(lambda j: (j[0], optlib.score_text(j[1])), jobs))
    res.sort(key=lambda x: (0 if x[1].get('identical') else x[1].get('total', 10 ** 9)))
    print('removals', rms)
    for f, r in res[:int(os.environ.get('TOP', 25))]:
        print('%-12s %s' % (' '.join(f), optlib.fmt(r)[:140]))


main()
