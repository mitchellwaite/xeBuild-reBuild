"""samp.py OUT N SEED [BASE.json] : random edit sets (1..K edits on top of BASE), real compiles; logs per
variant: score, loop-block subsequence inversions (LOOPB), the order and the edits (json lines)."""
import json, os, random, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voc, ev
out, N, SEED = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
base = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else []
random.seed(SEED)
K = int(os.environ.get('K', '4'))
SITES = [s for s in voc.SITES if voc.targets_for(s)]
if os.environ.get('NOINJ'): SITES = [s for s in SITES if not s.startswith('!')]
LOOPB = [55, 61, 33, 29, 67, 35, 42, 53, 77, 79]
LP = {b: i for i, b in enumerate(LOOPB)}


def linv(o):
    s = [b for b in o if b in LP]
    return sum(1 for a in range(len(s)) for b in range(a + 1, len(s)) if LP[s[a]] > LP[s[b]])


def one(i):
    e = [list(x) for x in base]
    used = set(x[0] for x in e)
    for _ in range(random.randint(1, K)):
        s = random.choice(SITES)
        if s in used: continue
        used.add(s); tg = voc.targets_for(s)
        e.append([s, random.sample(tg, min(len(tg), random.randint(1, 3)))])
    r = ev.ev(voc.make(e), '%s_%d' % (os.path.basename(out), i % 16), fncmp=False)
    return e, r


with ThreadPoolExecutor(4) as ex, open(out + '.jsonl', 'a') as f:
    for e, r in ex.map(one, range(N)):
        if r is None: continue
        f.write(json.dumps({'e': e, 'score': r['score'], 'linv': linv(r['o']), 'o': r['o'], 'miss': r['tmiss']}) + '\n')
        f.flush()
