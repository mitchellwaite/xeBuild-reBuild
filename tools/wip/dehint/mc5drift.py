"""mode_client attempt 5: pairs of near-miss removals on count-neutral (or near) natural
rewrites of the base ("drift bases").  Each rewrite is an mc5nat rule; the removals are
mc1 edits whose single diff on the base (MC2SINGLES) is <= -m.

python tools/wip/dehint/mc5drift.py [-m 22] [-j 4] RULE@K ...
Hits -> build/mc/m5drift_hits.json."""
import itertools, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc5nat

HITS = os.path.join(mc1lib.BUILD, 'm5drift_hits.json')


def main():
    a = sys.argv[1:]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    md = int(a[a.index('-m') + 1]) if '-m' in a else 22
    skip = set()
    for f in ('-j', '-m'):
        if f in a:
            skip |= {a.index(f), a.index(f) + 1}
    rules = [x for k, x in enumerate(a) if k not in skip]
    base = mc1lib.read_src(mc1.BASE)
    t = mc1.build_template(base)
    ed = {e[0]: e for e in mc1.edits(t)}
    sj = json.load(open(os.path.join(mc1lib.BUILD, os.environ.get('MC2SINGLES', 'm5_singles2.json'))))
    near = []
    for k, r in sj.items():
        m = re.match(r'(\d+)', r['r'])
        if k in ed and not mc5nat.SKIP.search(k) and not r['ok'] and m and int(m.group(1)) <= md:
            near.append(k)
    combos = [(k,) for k in near] + list(itertools.combinations(near, 2))
    todo = []
    for c in combos:
        st = ({}, {}, [])
        for k in c:
            st = st and mc1.merge(st, ed[k][1:])
        if not st:
            continue
        txt = mc1.render(t, *st)
        vs = dict(mc5nat.variants(txt, None))
        for r in rules:
            if r in vs:
                todo.append((' + '.join(c) + ' + ' + r, vs[r]))
    print(len(near), 'near,', len(todo), 'variants', flush=True)
    hits = json.load(open(HITS)) if os.path.exists(HITS) else {}
    n0 = mc1.count(base)['total']
    done = 0
    with ThreadPoolExecutor(jobs) as ex:
        for k, s, c in ex.map(mc5nat.mc3nat.score, todo):
            done += 1
            if s.get('identical'):
                print('HIT', k, c, '(base %d)' % n0, flush=True)
                hits[k] = c
                json.dump(hits, open(HITS, 'w'), indent=1)
            elif done % 500 == 0:
                print('..', done, flush=True)


if __name__ == '__main__':
    main()
