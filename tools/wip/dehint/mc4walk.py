"""mode_client attempt 4: walk = mc4greedy rounds, and when stuck, pairs of near misses
(diff <= -m) taking a count reducer if one exists, else a count-neutral pair (label drops),
then greedy again.  Stops after -rounds or when no pair matches.

python tools/wip/dehint/mc4walk.py BASE.c OUTPREFIX [-m 120] [-j 6] [-rounds 12]"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

SKIP = re.compile(r'^G_|^fk_all$|^rok_all$|^inline$|^-np$|^cold_.*=2$')


def singles(t, jobs):
    es = [e for e in mc1.edits(t) if not SKIP.search(e[0])]
    with ThreadPoolExecutor(jobs) as ex:
        return list(zip(es, ex.map(lambda e: mc1.score(t, *e[1:]), es)))


def main():
    a = sys.argv[1:]
    base = mc1lib.read_src(a[0])
    pre = a[1]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 6
    md = int(a[a.index('-m') + 1]) if '-m' in a else 120
    rounds = int(a[a.index('-rounds') + 1]) if '-rounds' in a else 12
    seen = set()
    for rnd in range(1, rounds + 1):
        t = mc1.build_template(base)
        n0 = mc1.count(base)['total']
        res = singles(t, jobs)
        free = sorted([(s['count'], e) for e, s in res if s.get('identical')], key=lambda x: x[0])
        cur = ({}, {}, [])
        took = []
        for c, e in free:
            m = mc1.merge(cur, e[1:])
            if m and mc1.score(t, *m).get('identical'):
                cur = m
                took.append(e[0])
        if took:
            base = mc1.render(t, *cur)
            out = '%s_%d.c' % (pre, rnd)
            open(out, 'w', newline='\n').write(base)
            print('ROUND', rnd, 'greedy', took, '->', mc1.count(base)['total'], out, flush=True)
            continue
        near = sorted((s['total'], e) for e, s in res
                      if 'total' in s and s['total'] and not s['identical'] and s['total'] <= md)
        todo = []
        for i in range(len(near)):
            for j in range(i + 1, len(near)):
                m = mc1.merge(({}, {}, []), near[i][1][1:])
                m = m and mc1.merge(m, near[j][1][1:])
                if m:
                    todo.append((near[i][1][0] + ' + ' + near[j][1][0], m))
        print('ROUND', rnd, len(near), 'near,', len(todo), 'pairs at', n0, flush=True)
        hits = []
        with ThreadPoolExecutor(jobs) as ex:
            for (k, m), s in zip(todo, ex.map(lambda e: mc1.score(t, *e[1]), todo)):
                if s.get('identical'):
                    print('PAIR', k, s['count'], flush=True)
                    hits.append((s['count'], k, m))
        hits = [h for h in sorted(hits, key=lambda h: h[0]) if h[1] not in seen]
        if not hits:
            print('STUCK at', n0, flush=True)
            break
        c, k, m = hits[0]
        seen.add(k)
        base = mc1.render(t, *m)
        out = '%s_%d.c' % (pre, rnd)
        open(out, 'w', newline='\n').write(base)
        print('ROUND', rnd, 'pair', k, '->', mc1.count(base)['total'], out, flush=True)


if __name__ == '__main__':
    main()
