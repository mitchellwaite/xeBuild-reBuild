"""mode_client attempt 4: greedy walk that also takes free label drops (count-neutral).
Each round: mc1 singles on the rendered base; take every free edit one at a time (count
reducers first, then label drops), keeping each that stays IDENTICAL; render; repeat until
a round takes nothing.  Label drops change edge counts into blocks, which is what opened
further removals after the E(reboot) change.

python tools/wip/dehint/mc4greedy.py BASE.c OUTPREFIX [-j N] [-rounds N]
Writes OUTPREFIX_<n>.c per round and prints what it took."""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

SKIP = re.compile(r'^G_|^fk_all$|^rok_all$|^inline$|^-np$')


def main():
    a = sys.argv[1:]
    base = mc1lib.read_src(a[0])
    pre = a[1]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 6
    rounds = int(a[a.index('-rounds') + 1]) if '-rounds' in a else 30
    for rnd in range(1, rounds + 1):
        t = mc1.build_template(base)
        n0 = mc1.count(base)['total']
        es = [e for e in mc1.edits(t) if not SKIP.search(e[0])]
        with ThreadPoolExecutor(jobs) as ex:
            res = list(zip(es, ex.map(lambda e: mc1.score(t, *e[1:]), es)))
        free = [(s['count'], e) for e, s in res if s.get('identical')]
        free.sort(key=lambda x: x[0])
        cur = ({}, {}, [])
        took = []
        for c, e in free:
            m = mc1.merge(cur, e[1:])
            if m and mc1.score(t, *m).get('identical'):
                cur = m
                took.append(e[0])
        if not took:
            print('ROUND', rnd, 'nothing free at', n0, flush=True)
            break
        base = mc1.render(t, *cur)
        out = '%s_%d.c' % (pre, rnd)
        open(out, 'w', newline='\n').write(base)
        print('ROUND', rnd, 'took', took, '->', mc1.count(base)['total'], out, flush=True)


if __name__ == '__main__':
    main()
