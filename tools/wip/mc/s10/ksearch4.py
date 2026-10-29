"""real-valued design search on the b40 history: chains capped at 50%, C<=CMAX.
python ksearch4.py bbro iters seed"""
import random, sys, os, json
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\tools\wip'); sys.path.insert(0, ROOT + r'\tools\wip\mc'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fibsim, fibwhatif, mcsim3
ev = fibsim.parse(sys.argv[1]); R = fibwhatif.groups(ev)
npre = sum(len(r['order']) for r in R[:3])
CMAX = float(os.environ.get('CMAX', '7.45')); CAP = float(os.environ.get('CAP', '0.5'))
rd = lambda v: int(v + 0.5)
K = {'C': (5, CMAX), 'h1': (0, CAP), 'h2': (0, CAP), 'e2': (0, 1), 'e3': (0, CAP), 'e4': (0, CAP), 'v49': (4, 9.49), 'a': (0, CAP), 'b': (0, CAP), 'c': (0, CAP),
     'u2': (0, 9.4), 'p117': (0, 1), 'p130': (0, 1), 'u29': (0, 9), 'u33': (0, 9), 'u35': (0, 5), 'u42': (0, 5), 'u53': (0, 5), 'u77': (0, 5), 'u79': (0, 5)}
def freqs(x):
    C = x['C']; f = {}
    f[112] = rd(C * x['h1']); f[115] = rd(C * x['h2'])
    i = C * x['e2']; f[127] = rd(i); r1 = C - i
    o = r1 * x['e3']; f[126] = rd(o); r2 = r1 - o
    f[125] = rd(r2 * x['e4'])
    f[49] = rd(x['v49']); v55 = x['v49'] * x['a']; f[55] = rd(v55); v61 = v55 * x['b']; f[61] = rd(v61); f[67] = rd(v61 * x['c'])
    f[103] = rd(x['u2']); f[117] = rd(C * x['p117']); f[130] = rd(C * x['p130'])
    for b in (29, 33, 35, 42, 53, 77, 79): f[b] = rd(x['u%d' % b])
    return f
def score(x):
    o = mcsim3.sim(R, freqs(x)); pre, inv, oo = mcsim3.score(o, npre)
    return inv, pre, oo
random.seed(int(sys.argv[3])); best = None; bs = (999,)
for it in range(int(sys.argv[2])):
    if best is None or random.random() < 0.02:
        x = {k: random.uniform(*v) for k, v in K.items()}
    else:
        x = dict(best)
        for k in random.sample(list(K), random.choice((1, 1, 2, 3))):
            lo, hi = K[k]; x[k] = min(hi, max(lo, x[k] + random.gauss(0, (hi - lo) / 6)))
    inv, pre, oo = score(x)
    if (inv, -pre) <= bs:
        if (inv, -pre) < bs: print(it, inv, pre, freqs(x), flush=True)
        bs, best = (inv, -pre), x
        if inv == 0: break
print('best', bs, json.dumps(best)); print(freqs(best)); print(' '.join(map(str, score(best)[2])))
