"""mode_client attempt 3: hint removal x natural rewrite.  Singles of mc1's edits on BASE
(cached in build/mc/m3nx_singles_<basename>.json); each near miss (diff <= -m, default 30)
is rendered and every mc3nat rewrite is tried on top.  Also (-n) rewrite pairs on the base.

python tools/wip/dehint/mc3nx.py BASE.c [-m 30] [-j 4] [-r RULE_REGEX]
IDENTICAL hits print with the trick count and go to build/mc/m3nx_hits.json."""
import json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc3nat

SKIP = re.compile(r'fa([3-9]|1[0-9]|20)$|^G_|^fk_all$|^-np$|^rok_all$|^inline$')
HITS = os.path.join(mc1lib.BUILD, 'm3nx_hits.json')


def main():
    a = sys.argv[1:]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    md = int(a[a.index('-m') + 1]) if '-m' in a else 30
    rx = a[a.index('-r') + 1] if '-r' in a else None
    basef = a[0]
    base = mc1lib.read_src(basef)
    n0 = mc1.count(base)['total']
    t = mc1.build_template(base)
    cache = os.path.join(mc1lib.BUILD, 'm3nx_singles_%s.json' % os.path.basename(basef))
    es = [e for e in mc1.edits(t) if not SKIP.search(e[0])]
    if os.path.exists(cache):
        sing = json.load(open(cache))
    else:
        sing = {}
        with ThreadPoolExecutor(jobs) as ex:
            for e, s in zip(es, ex.map(lambda e: mc1.score(t, *e[1:]), es)):
                sing[e[0]] = {'total': s.get('total'), 'identical': s.get('identical'),
                              'count': s.get('count')}
        json.dump(sing, open(cache, 'w'), indent=1)
    free = [k for k, s in sing.items() if s['identical'] and s['count'] < n0]
    if free:
        print('FREE singles:', free, flush=True)
    near = sorted((s['total'], k) for k, s in sing.items()
                  if s['total'] is not None and not s['identical'] and s['total'] <= md)
    print(len(near), 'near misses', flush=True)
    ed = {e[0]: e for e in es}
    todo = []
    for d, k in near:
        txt = mc1.render(t, *ed[k][1:])
        for vn, v in mc3nat.variants(txt, rx):
            todo.append(('%s + %s' % (k, vn), v))
    print(len(todo), 'variants', flush=True)
    hits = json.load(open(HITS)) if os.path.exists(HITS) else {}
    done = 0
    with ThreadPoolExecutor(jobs) as ex:
        for k, s, c in ex.map(mc3nat.score, todo):
            done += 1
            if s.get('identical'):
                print('HIT', k, c, flush=True)
                hits['%s %s' % (basef, k)] = c
                json.dump(hits, open(HITS, 'w'), indent=1)
            elif done % 500 == 0:
                print('..', done, flush=True)


if __name__ == '__main__':
    main()
