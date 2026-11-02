"""ga.py OUT GENS SEED [seed jsonl files...] : steady-state genetic search over voc edit sets, real
compiles (4 threads).  Objective score*1000 + fncmp (score = true inv + 5*missing).  Crossover =
random subset of the union of two parents' edits (one per site); mutation = ls.py moves.
Logs improvements to OUT.log, population to OUT.pop.json."""
import json, os, random, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voc, ev
out, GENS, SEED = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
random.seed(SEED)
POP = int(os.environ.get('POP', '40'))
MAXT = 3
SITES = [s for s in voc.SITES if voc.targets_for(s)]
log = open(out + '.log', 'a')
import itertools
cnt = itertools.count()


def obj(r):
    return 10 ** 9 if r is None else r['score'] * 1000 + (r.get('fncmp') or 0)


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


def run(e):
    tag = '%s_%d' % (os.path.basename(out), next(cnt) % 12)
    try:
        return e, ev.ev(voc.make(e), tag)
    except Exception:
        return e, None


seeds = []
for fn in sys.argv[4:]:
    if fn.endswith('.jsonl'):
        L = [json.loads(l) for l in open(fn)]
        L.sort(key=lambda x: x['score'])
        seeds += [x['e'] for x in L[:POP]]
    else:
        seeds.append(json.load(open(fn)))
while len(seeds) < POP: seeds.append(mutate(random.choice(seeds) if seeds else []))
seeds = seeds[:POP]
with ThreadPoolExecutor(4) as ex:
    pop = [(obj(r), e, r) for e, r in ex.map(run, seeds)]
    pop.sort(key=lambda x: x[0])
    best = pop[0][0]
    print('init', best, json.dumps(pop[0][1]), file=log, flush=True)
    for g in range(GENS):
        kids = []
        for _ in range(8):
            a = min(random.sample(pop, 3), key=lambda x: x[0])[1]
            b = min(random.sample(pop, 3), key=lambda x: x[0])[1]
            c = cross(a, b) if random.random() < 0.5 else [list(x) for x in a]
            for _ in range(random.choice((1, 1, 2))): c = mutate(c)
            kids.append(c)
        for e, r in ex.map(run, kids):
            o = obj(r)
            if o >= 10 ** 9: continue
            if any(json.dumps(sorted(map(tuple, map(lambda x: (x[0], tuple(x[1])), e)))) ==
                   json.dumps(sorted(map(tuple, map(lambda x: (x[0], tuple(x[1])), p[1])))) for p in pop): continue
            if o < pop[-1][0]:
                pop[-1] = (o, e, r); pop.sort(key=lambda x: x[0])
            if o < best:
                best = o
                print(g, o, json.dumps(e), ' '.join(map(str, r['o'])), file=log, flush=True)
        if g % 20 == 0:
            json.dump([(p[0], p[1]) for p in pop], open(out + '.pop.json', 'w'))
print('done', best, file=log, flush=True)
