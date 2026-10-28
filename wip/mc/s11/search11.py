"""hill-climb over the s9 knobs + in-loop usage edges; objective fncmp*1000+inv.
python search10.py N seed   (log: wip/mc/s10/search10.log, best: .best)"""
import json, os, random, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import run
P = {'M': (1, 40), 'A': (50.2, 60), 'H1': (40, 50), 'H2': (40, 50), 'd1': (0.5, 50), 'd2': (0.5, 50), 'e2': (1, 50),
     'e3': (5, 50), 'e4': (5, 60), 'ip': (15, 40), 'r': (10, 50), 'w': (10, 50), 'e': (10, 50)}
for e in ('16>17', '19>20', '21>22', '28>29', '32>33', '34>35', '40>41', '42>43', '15>17', '14>17', '18>20', '31>33', '27>29', '53>54', '61>62', '77>78', '85>86'):
    P['mode_client:' + e] = (0, 1.5)
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ.get('SLOG', 'search11.log'))
def score(slot, x):
    f, inv, pre, _ = run.run(slot, x)
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
                for k in random.sample(list(P), random.choice((1, 1, 2))):
                    lo, hi = P[k]
                    cur = x.get(k, lo)
                    x[k] = round(min(hi, max(lo, cur + random.gauss(0, (hi - lo) / 5))), 3)
                cands.append(x)
            res = list(ex.map(lambda a: score('h%d' % (a[0] + 1), a[1]), enumerate(cands)))
            for x, (s, f, inv) in zip(cands, res):
                log.write('%d %d %d %s\n' % (s, f, inv, json.dumps(x)))
                if s <= bs:
                    if s < bs: print(it, f, inv, flush=True)
                    bs, best = s, x
                    json.dump(best, open(LOG + '.best', 'w'))
                    if f == 0: print('MATCH', x); return
            log.flush()
    print('best', bs, best)
main()
