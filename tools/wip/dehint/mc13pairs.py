"""mode_client attempt 13: pairs of single removals (mc12rm.variants + mc13neg.EXTRA) whose
block shifts add up to 0 or +1 mod 13 (the reference thread order), scored.

python tools/wip/dehint/mc13pairs.py BASE.c [-j 4] [-max 400]"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc12filt, mc12rm, mc13neg


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    mx = int(a[a.index('-max') + 1]) if '-max' in a else 400
    rms = [(k, None, None) for k, _ in mc12rm.variants(t)]
    # rebuild removals as (key, start, old, new) so two can be applied together
    import re
    eds = []
    s0 = t.index('static void clientEraseBlockI(')
    for kind, rx, rep in mc12rm.PATS:
        for m in re.finditer(rx, t):
            if m.start() >= s0:
                eds.append(('%s@%d' % (kind, m.start()), m.start(), m.end(), re.sub(rx, rep, m.group(0))))
    for k, o, n in mc13neg.EXTRA:
        if o in t:
            i = t.index(o)
            eds.append((k, i, i + len(o), n))

    def apply(es):
        x = t
        for k, s, e, n in sorted(es, key=lambda z: -z[1]):
            x = x[:s] + n + x[e:]
        return x

    def score1(es):
        x = apply(es)
        try:
            th = mc12vrp.threads(x)
        except Exception:
            return es, None, None
        if not mc12filt.good(th):
            return es, th, None
        return es, th, mc1lib.score_text(x, [])
    pairs = [p for p in itertools.combinations(eds, 2) if p[0][2] <= p[1][1] or p[1][2] <= p[0][1]]
    print(len(pairs), 'pairs', flush=True)
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(score1, pairs))
    rows = sorted((0 if s.get('identical') else s.get('total', 99999), ' + '.join(k for k, *_ in es)) for es, th, s in res if s)
    print(len(rows), 'with the reference thread order', flush=True)
    for d, k in rows[:30]:
        print(d, k, flush=True)


if __name__ == '__main__':
    main()
