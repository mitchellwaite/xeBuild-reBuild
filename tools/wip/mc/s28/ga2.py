"""ga2.py OUT GENS SEED [seeds...] : ga.py with a 'potential' objective: each variant is compiled
(real history) and pot.potential() enumerates f of the non-loop tail blocks 126 125 127 117 130 in
hsim (bcp injections change f without adding bbro events).  Objective = pot*1000 + score*10 +
fncmp/100.  Process pool (hsim has module state)."""
import json, os, random, sys, itertools
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voc, ev

MAXT = 3


def run(args):
    e, tag = args
    try:
        import pot
        r = ev.ev(voc.make(e), tag)
        if r is None: return e, None
        b = pot.potential2(tag) if os.environ.get('POT2') else pot.potential(tag)
        r['pot'] = b[0]; r['potd'] = [b[1], str(b[2]), b[3]]
        return e, r
    except Exception as x:
        return e, None


def obj(r):
    return 10 ** 9 if r is None else r['pot'] * 1000 + r['score'] * 10 + (r.get('fncmp') or 0) / 100


def main():
    out, GENS, SEED = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    random.seed(SEED)
    POP = int(os.environ.get('POP', '30'))
    SITES = [s for s in voc.SITES if voc.targets_for(s)]
    log = open(out + '.log', 'a')
    cnt = itertools.count()

    def mutate(e):
        e = [list(x) for x in e]
        k = random.random()
        if not e or k < 0.45:
            s = random.choice(SITES)
            if s not in [x[0] for x in e]:
                tg = voc.targets_for(s); e.append([s, random.sample(tg, min(len(tg), random.randint(1, MAXT)))])
        elif k < 0.7:
            e.pop(random.randrange(len(e)))
        else:
            i = random.randrange(len(e)); s = e[i][0]; tg = voc.targets_for(s)
            e[i][1] = random.sample(tg, min(len(tg), random.randint(1, MAXT)))
        return e

    def cross(a, b):
        d = {}
        for s, t in a + b:
            if s not in d or random.random() < 0.5: d[s] = t
        return [[s, t] for s, t in d.items() if random.random() < 0.7]

    def tagged(es):
        return [(e, '%s_%d' % (os.path.basename(out), next(cnt) % 16)) for e in es]

    seeds = []
    for fn in sys.argv[4:]:
        if fn.endswith('.jsonl'):
            L = [json.loads(l) for l in open(fn)]
            L.sort(key=lambda x: x.get('pot', x['score']))
            seeds += [x['e'] for x in L[:POP]]
        else:
            seeds.append(json.load(open(fn)))
    while len(seeds) < POP: seeds.append(mutate(random.choice(seeds) if seeds else []))
    seeds = seeds[:POP]
    key = lambda e: json.dumps(sorted((x[0], sorted(x[1])) for x in e))
    with ProcessPoolExecutor(4) as ex:
        pop = [(obj(r), e, r) for e, r in ex.map(run, tagged(seeds))]
        pop.sort(key=lambda x: x[0])
        best = pop[0][0]
        print('init', best, json.dumps(pop[0][1]), pop[0][2] and pop[0][2].get('potd'), file=log, flush=True)
        for g in range(GENS):
            kids = []
            for _ in range(8):
                a = min(random.sample(pop, 3), key=lambda x: x[0])[1]
                b = min(random.sample(pop, 3), key=lambda x: x[0])[1]
                c = cross(a, b) if random.random() < 0.5 else [list(x) for x in a]
                for _ in range(random.choice((1, 1, 2))): c = mutate(c)
                kids.append(c)
            try:
                res = list(ex.map(run, tagged(kids)))
            except Exception as x:
                print('pool error', repr(x)[:100], file=log, flush=True)
                ex.shutdown(wait=False, cancel_futures=True)
                ex = ProcessPoolExecutor(4)
                continue
            for e, r in res:
                o = obj(r)
                if o >= 10 ** 9: continue
                if any(key(e) == key(p[1]) for p in pop): continue
                if o < pop[-1][0]:
                    pop[-1] = (o, e, r); pop.sort(key=lambda x: x[0])
                if o < best:
                    best = o
                    print(g, round(o, 2), 'pot', r['pot'], 'score', r['score'], 'fncmp', r.get('fncmp'), json.dumps(e),
                          json.dumps(r['potd']), file=log, flush=True)
            if g % 10 == 0:
                json.dump([(p[0], p[1]) for p in pop], open(out + '.pop.json', 'w'))
    print('done', best, file=log, flush=True)


if __name__ == '__main__':
    main()
