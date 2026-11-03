"""python tools/wip/dehint/iwrand.py <seconds> <seed> trick1,trick2,... : random sampling of the neutral shapes
in iwanneal.SHAPES with these tricks removed.  Prints every identical state (and writes build/iw/rand_<tricks>.c)
and the best score seen."""
import json, os, random, sys, time
from concurrent.futures import ThreadPoolExecutor
secs, seed, tr = int(sys.argv[1]), int(sys.argv[2]), [x for x in sys.argv[3].split(',') if x]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = ['x']
import iwanneal as A, iwlib

NEUTRAL = {'first': [1, 2], 'range': [1, 3], 'memset': [1, 2], 'if_p': [2], 's9': [1], 'fsend': [1, 2], 'nloop': [1],
           'lim': [1], 'test': [2], 'next': [1, 2], 't': [1], 'pages': [1, 2, 3], 'tail': [1, 3], 'wf_loop': [1],
           'wf_big': [1], 'wf_small': [1], 'big_lba': [1], 'bigarg': [1], 'end': [1, 2], 'blkvar': [1, 2, 3], 'type0': [1],
           'imgend': [1], 'wf_blk': [1, 2]}
rnd = random.Random(seed)
keys = list(NEUTRAL)


def sample():
    s = {t: True for t in tr}
    s.update(json.loads(os.environ.get("IWFIX", "{}")))
    for k in keys:
        if k in json.loads(os.environ.get("IWFIX", "{}")):
            continue
        if rnd.random() < 0.3:
            s[k] = rnd.choice(NEUTRAL[k])
    return s


t0 = time.time()
best = 10 ** 9
n = 0
found = 0
with ThreadPoolExecutor(4) as ex:
    while time.time() - t0 < secs and found < 3:
        cands = [sample() for _ in range(8)]
        for s, (v, r) in ex.map(lambda s: (s, A.score(s)), cands):
            n += 1
            if r.get('identical'):
                found += 1
                print('IDENTICAL', json.dumps(s), flush=True)
                open(os.path.join(iwlib.BUILD, 'rand_%s.c' % '_'.join(tr)), 'w', newline='\n').write(A.render(s))
                json.dump(s, open(os.path.join(iwlib.BUILD, 'rand_%s.json' % '_'.join(tr)), 'w'))
            elif r.get('total', 10 ** 9) < best:
                best = r['total']
                print(best, json.dumps({k: x for k, x in s.items()}), iwlib.fmt(r)[:120], flush=True)
print('tried', n, 'best', best)
