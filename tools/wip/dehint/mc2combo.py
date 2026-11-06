"""mode_client attempt 2: score every combination of mc1 states (one per group) on the base.

python tools/wip/dehint/mc2combo.py HITS.json [HITS2.json ...]
Each file is a {name: {state, drops, post}} map (mc2.py's m2_hits.json); one entry from each
file is merged and scored.  IDENTICAL combinations are printed."""
import itertools, json, os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib


def main():
    groups = [list(json.load(open(p)).items()) for p in sys.argv[1:]]
    t = mc1.build_template(mc1lib.read_src(mc1.BASE))
    todo = []
    for combo in itertools.product(*groups):
        m = ({}, {}, [])
        for _, h in combo:
            m = m and mc1.merge(m, (h['state'], h['drops'], h.get('post', [])))
        if m:
            todo.append((' | '.join(k for k, _ in combo), m))
    with ThreadPoolExecutor(4) as ex:
        for (k, m), s in zip(todo, ex.map(lambda e: mc1.score(t, *e[1]), todo)):
            print('%s %s %s' % ('HIT' if s.get('identical') else '   ', s['count'], k), mc1lib.fmt(s)[:60], flush=True)
            if s.get('identical'):
                json.dump({'state': m[0], 'drops': m[1], 'post': m[2]}, open(os.path.join(mc1lib.BUILD, 'm2combo_best.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
