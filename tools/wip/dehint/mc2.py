"""mode_client attempt 2: singles, wide pairs and triples of mc1's edits on the current base.

python tools/wip/dehint/mc2.py singles [-j N]            -> build/mc/m2_singles.json
python tools/wip/dehint/mc2.py pairs [-m DIFF] [-j N]    near misses (diff <= DIFF) in pairs
python tools/wip/dehint/mc2.py triples [-m DIFF] [-j N]  near misses (diff <= DIFF) in triples
python tools/wip/dehint/mc2.py near [-m DIFF]            list the near misses
Base: src/mode_client.c or MCBASE=<file> (mc1's template; names carry mc1's running index).
Each IDENTICAL combination is printed and saved in build/mc/m2_hits.json."""
import itertools, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

OUT = mc1lib.BUILD
SJ = os.path.join(OUT, os.environ.get('MC2SINGLES', 'm2_singles.json'))
HITS = os.path.join(OUT, 'm2_hits.json')


def near(maxdiff):
    sj = json.load(open(SJ))
    out = []
    for k, r in sj.items():
        m = re.match(r'(\d+)', r['r'])
        if not r['ok'] and m and int(m.group(1)) <= maxdiff:
            out.append((int(m.group(1)), k))
    ex = os.environ.get('MC2SKIP')
    if ex:
        out = [x for x in out if not re.search(ex, x[1])]
    return [k for _, k in sorted(out)]


def combos(t, start, keys, n):
    es = {e[0]: e for e in mc1.edits(t)}
    todo = []
    for c in itertools.combinations(keys, n):
        m = start
        for k in c:
            m = m and mc1.merge(m, es[k][1:])
        if m:
            todo.append((' + '.join(c), m))
    return todo


def run(t, todo, jobs):
    hits = json.load(open(HITS)) if os.path.exists(HITS) else {}
    print(len(todo), 'combinations', flush=True)
    done = 0
    with ThreadPoolExecutor(jobs) as ex:
        for (k, m), s in zip(todo, ex.map(lambda e: mc1.score(t, *e[1]), todo)):
            done += 1
            if s.get('identical'):
                print('HIT', k, s['count'], flush=True)
                hits[k] = {'state': m[0], 'drops': m[1], 'post': m[2], 'count': s['count']}
                json.dump(hits, open(HITS, 'w'), indent=1)
            elif done % 200 == 0:
                print('..', done, flush=True)
    return hits


def main():
    a = sys.argv[1:]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    md = int(a[a.index('-m') + 1]) if '-m' in a else 30
    t = mc1.build_template(mc1lib.read_src(mc1.BASE))
    start = ({}, {}, [])
    if '-s' in a:
        j = json.load(open(a[a.index('-s') + 1]))
        start = (j['state'], j['drops'], j.get('post', []))
    if a[0] == 'singles':
        res = mc1.run_singles(t, jobs, start)
        json.dump(res, open(SJ, 'w'), indent=1)
    elif a[0] == 'near':
        for k in near(md):
            print(json.load(open(SJ))[k]['r'][:120], k)
    elif a[0] == 'pairs':
        run(t, combos(t, start, near(md), 2), jobs)
    elif a[0] == 'triples':
        run(t, combos(t, start, near(md), 3), jobs)


if __name__ == '__main__':
    main()
