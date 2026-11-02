"""ls.py OUT START.json ITERS SEED : parallel stochastic local search over asm-goto edit sets
(voc.py vocabulary), real compiles, objective score*1000 + fncmp (score = true inv + 5*missing).
Writes OUT.log (improvements) and OUT.best.json."""
import json, os, random, sys, math
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voc, ev
out, start, IT, SEED = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
random.seed(SEED)
NW = int(os.environ.get('NW', '4'))
MAXT = int(os.environ.get('MAXT', '3'))
SITES = [s for s in voc.SITES if voc.targets_for(s)]
if os.environ.get('SITES'): SITES = [s for s in SITES if s in os.environ['SITES'].split(',')]
cur = json.load(open(start)) if os.path.exists(start) else []
log = open(out + '.log', 'a')


def obj(r):
    return 10 ** 9 if r is None else r['score'] * 1000 + (r.get('fncmp') or 0)


def mutate(e):
    e = [list(x) for x in e]
    k = random.random()
    if not e or k < 0.45:
        s = random.choice(SITES); tg = voc.targets_for(s)
        e.append([s, random.sample(tg, min(len(tg), random.randint(1, MAXT)))])
    elif k < 0.7:
        e.pop(random.randrange(len(e)))
    else:
        i = random.randrange(len(e)); s = e[i][0]; tg = voc.targets_for(s)
        e[i][1] = random.sample(tg, min(len(tg), random.randint(1, MAXT)))
    sites = [x[0] for x in e]
    if len(set(sites)) != len(sites): return None
    return e


def run(args):
    e, tag = args
    try:
        return e, ev.ev(voc.make(e), tag)
    except Exception as x:
        return e, None


r0 = run((cur, '%s_0' % os.path.basename(out)))[1]
best = obj(r0); bcur = cur
print('start', best, cur, file=log, flush=True)
T0 = float(os.environ.get('T0', '1500'))
with ThreadPoolExecutor(NW) as ex:
    for it in range(IT):
        cands = []
        while len(cands) < NW:
            c = mutate(cur)
            if c is not None: cands.append((c, '%s_w%d' % (os.path.basename(out), len(cands))))
        res = list(ex.map(run, cands))
        res.sort(key=lambda x: obj(x[1]))
        e, r = res[0]
        T = T0 * (1 - it / IT) + 1
        o = obj(r)
        if o < obj(r0) or random.random() < math.exp((obj(r0) - o) / T):
            cur, r0 = e, r
            if o < best:
                best, bcur = o, e
                print(it, o, json.dumps(e), ' '.join(map(str, r['o'])), file=log, flush=True)
                json.dump(bcur, open(out + '.best.json', 'w'))
print('done', best, json.dumps(bcur), file=log, flush=True)
