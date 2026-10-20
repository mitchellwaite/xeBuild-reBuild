"""Search edge probabilities for wip/mufdo.sh (fewest fncmp lines).

python wip/mufdo_search.py <dir> greedy|random [seed iterations] [fn:src>dst=prob ...]

greedy scales the minor arm of each two-way branch of mode_update and
updateNand (one at a time, first improvement wins, repeat); random changes
2-3 of them per step. Starts from the given overrides. Use one <dir> per
concurrent run (each has its own .gcda).
"""
import random, re, subprocess, sys
sys.path.insert(0, 'wip')
import gcda


def main():
    d, mode = sys.argv[1], sys.argv[2]
    rest = sys.argv[3:]
    seed, iters = (int(rest[0]), int(rest[1])) if mode == 'random' else (0, 0)
    if mode == 'random':
        rest = rest[2:]
    over = {}
    for a in rest:
        m = re.match(r'(\w+):(\d+)>(\d+)=([\d.]+)$', a)
        over[(m.group(1), int(m.group(2)), int(m.group(3)))] = float(m.group(4))
    cache = {}

    def score(o):
        key = tuple(sorted(o.items()))
        if key not in cache:
            args = ['%s:%d>%d=%.2f' % (f, s, t, p) for (f, s, t), p in o.items()]
            r = subprocess.run(['sh', 'wip/mufdo.sh', d] + args, capture_output=True, text=True)
            out = r.stdout.strip().split('\n')[-1]
            cache[key] = int(out) if out.isdigit() else 9999
            if 'error' in open(d + '/fdo.diff').read()[:3000]:
                cache[key] = 9999
        return cache[key]

    best = score(over)
    print('start', best, flush=True)
    est, calls = gcda.read_dump(d + '/m.c.042t.profile_estimate')
    edges = []
    for fn in ('mode_update', 'updateNand'):
        for b, (freq, succ) in sorted(est[fn].items()):
            if len(succ) == 2:
                (d0, p0), (d1, p1) = succ.items()
                edges.append((fn, b) + ((d0, p0) if p0 <= p1 else (d1, p1)))
    fact = [0.3, 0.5, 0.7, 0.85, 0.93, 1.07, 1.2, 1.5, 2.0, 3.0]
    show = lambda: {'%s:%d>%d' % k: round(v, 2) for k, v in over.items()}
    if mode == 'greedy':
        improved = True
        while improved and best:
            improved = False
            for fn, b, t, p in edges:
                k = (fn, b, t)
                for f in fact:
                    trial = dict(over)
                    trial[k] = min(99.0, max(0.5, over.get(k, p) * f))
                    n = score(trial)
                    if n < best:
                        best, over, improved = n, trial, True
                        print(best, show(), flush=True)
                        break
    else:
        random.seed(seed)
        for it in range(iters):
            if not best:
                break
            trial = dict(over)
            for fn, b, t, p in random.sample(edges, random.choice([2, 2, 3])):
                k = (fn, b, t)
                trial[k] = min(99.0, max(0.5, over.get(k, p) * random.choice(fact)))
            n = score(trial)
            if n < best:
                best, over = n, trial
                print(it, best, show(), flush=True)
    print('final', best, show())


if __name__ == '__main__':
    main()
