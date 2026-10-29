"""hill-climb for the asm-goto fake-edge variant (vY): s11 knobs + case weights + fake probs.
python search12.py N seed   env SLOG (log name), START (json), MCD (mcvY)"""
import json, os, random, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import run12
P = {'M': (1, 40), 'A': (40, 60), 'H1': (5, 50), 'H2': (5, 50), 'd1': (0.5, 50), 'd2': (0.5, 50), 'e2': (1, 50),
     'e3': (5, 50), 'e4': (5, 50), 'ip': (15, 40), 'r': (10, 50), 'w': (10, 50), 'e': (10, 50)}
for e in ('16>17', '19>20', '21>22', '28>29', '32>33', '34>35', '40>41', '42>43', '15>17', '14>17', '18>20', '31>33', '27>29', '53>54', '61>62', '77>78', '85>86'):
    P['mode_client:' + e] = (0, 1.5)
CASES = [114, 115, 116, 117, 120, 123, 126, 127, 128, 129, 130, 133]
DISP = int(os.environ.get('DISP', '113')); XB = int(os.environ.get('XB', '112'))
FAKES = [int(t) for t in os.environ.get('FAKES', '119 122 128').split()]
for c in CASES: P['cw%d' % c] = (0.2, 3)
for t in FAKES: P['fx%d' % t] = (0, 15)
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ.get('SLOG', 'search12.log'))
def design(x):
    d = {k: v for k, v in x.items() if not (k.startswith('cw') or k.startswith('fx'))}
    tot = sum(x.get('cw%d' % c, 1) for c in CASES)
    for c in CASES: d['raw:mode_client:%d>%d' % (DISP, c)] = 100.0 * x.get('cw%d' % c, 1) / tot
    for t in FAKES: d['raw:mode_client:%d>%d' % (XB, t)] = x.get('fx%d' % t, 0)
    return d
def score(slot, x):
    f, inv, pre, _ = run12.run(slot, design(x))
    return f * 1000 + inv, f, inv
def main():
    n = int(sys.argv[1]); random.seed(int(sys.argv[2]))
    best = json.load(open(LOG + '.best')) if os.path.exists(LOG + '.best') else json.load(open(os.environ['START']))
    bs = score('h0', best)[0]; print('start', bs, flush=True)
    log = open(LOG, 'a')
    with ThreadPoolExecutor(4) as ex:
        for it in range(n):
            cands = []
            for j in range(4):
                x = dict(best)
                for k in random.sample(list(P), random.choice((1, 1, 2, 3))):
                    lo, hi = P[k]
                    cur = x.get(k, 1 if k.startswith('cw') else lo)
                    x[k] = round(min(hi, max(lo, cur + random.gauss(0, (hi - lo) / 5))), 3)
                cands.append(x)
            res = list(ex.map(lambda a: score('h%d' % (a[0] + 1), a[1]), enumerate(cands)))
            for x, (s, f, inv) in zip(cands, res):
                log.write('%d %d %d %s\n' % (s, f, inv, json.dumps(x)))
                if s <= bs:
                    if s < bs: print(it, f, inv, flush=True)
                    bs, best = s, x
                    json.dump(best, open(LOG + '.best', 'w'))
                    if f == 0: print('MATCH', x, flush=True); return
            log.flush()
    print('best', bs, best)
main()
