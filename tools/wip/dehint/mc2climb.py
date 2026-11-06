"""mode_client attempt 2: climb on rendered bases.  Each round: singles on the base, greedy
over the free ones, then pairs of near misses (diff <= -m, default 250); take the pair
that removes the most, render it as the next base (build/mc/climb2_<n>.c) and repeat.

python tools/wip/dehint/mc2climb.py BASE.c [-m 250] [-j 4] [-rounds N]"""
import json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc2

OUT = mc1lib.BUILD
SKIP = re.compile(r'fa([3-9]|1[0-9]|20)$|^G_|^fk_all$')


def singles(t, jobs):
    res = {}
    es = [e for e in mc1.edits(t) if not SKIP.search(e[0])]
    with ThreadPoolExecutor(jobs) as ex:
        for e, s in zip(es, ex.map(lambda e: mc1.score(t, *e[1:]), es)):
            res[e[0]] = (s, e)
    return res


def gain_state(t, st, n0):
    return n0 - mc1.count(mc1.render(t, *st))['total']


def main():
    a = sys.argv[1:]
    base = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    md = int(a[a.index('-m') + 1]) if '-m' in a else 250
    rounds = int(a[a.index('-rounds') + 1]) if '-rounds' in a else 20
    for rnd in range(1, rounds + 1):
        t = mc1.build_template(base)
        n0 = mc1.count(base)['total']
        res = singles(t, jobs)
        cur = ({}, {}, [])
        free = [k for k, (s, e) in res.items() if s.get('identical') and gain_state(t, mc1.merge(cur, e[1:]) or cur, n0) > 0]
        for k in free:
            m = mc1.merge(cur, res[k][1][1:])
            if m and mc1.score(t, *m).get('identical'):
                cur = m
                print('FREE', k, flush=True)
        if cur != ({}, {}, []):
            base = mc1.render(t, *cur)
            open(os.path.join(OUT, 'climb2_%d.c' % rnd), 'w', newline='\n').write(base)
            print('ROUND', rnd, 'greedy ->', mc1.count(base)['total'], flush=True)
            continue
        near = sorted((int(re.match(r'(\d+)', mc1lib.fmt(s)).group(1)), k) for k, (s, e) in res.items()
                      if 'total' in s and not s['identical'] and s['total'] <= md)
        keys = [k for _, k in near]
        todo = []
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                m = mc1.merge(({}, {}, []), res[keys[i]][1][1:])
                m = m and mc1.merge(m, res[keys[j]][1][1:])
                if m:
                    todo.append((keys[i] + ' + ' + keys[j], m))
        print('ROUND', rnd, len(keys), 'near,', len(todo), 'pairs', flush=True)
        best = None
        with ThreadPoolExecutor(jobs) as ex:
            for (k, m), s in zip(todo, ex.map(lambda e: mc1.score(t, *e[1]), todo)):
                if s.get('identical'):
                    g = gain_state(t, m, n0)
                    print('PAIR', k, g, flush=True)
                    if g > 0 and (best is None or g > best[0]):
                        best = (g, k, m)
        if not best:
            print('STUCK at', n0, flush=True)
            break
        base = mc1.render(t, *best[2])
        open(os.path.join(OUT, 'climb2_%d.c' % rnd), 'w', newline='\n').write(base)
        print('TAKE', best[1], '->', mc1.count(base)['total'], flush=True)


if __name__ == '__main__':
    main()
