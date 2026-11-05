"""score every subset of the given trick names (smallest totals first).
python opsub.py a b c ... [-k N]  (subsets of size >= 2, best N shown, default 25)"""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks


def main():
    a = sys.argv[1:]
    k = 25
    if '-k' in a:
        i = a.index('-k')
        k = int(a[i + 1])
        del a[i:i + 2]
    names = optricks.expand(a)
    b = optricks.base()
    combos = [c for r in range(2, len(names) + 1) for c in itertools.combinations(names, r)]
    with optricks.pool() as p:
        rs = list(p.map(lambda c: (c, optricks.score(list(c), b)), combos))
    rs.sort(key=lambda x: (x[1].get('total', 10**9), -len(x[0])))
    for c, r in rs[:k]:
        print('%-50s %s' % ('+'.join(c), optlib.fmt(r)[:110]))


main()
