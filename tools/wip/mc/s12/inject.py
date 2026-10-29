"""What-if: inject a dummy heap node (an extra cold block) into the b.txt history and
hill-climb the s10 ksearch4 design space; does any injection admit inv 0?
python inject.py bbro iters [CMAX env]"""
import copy, random, sys, os
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\tools\wip'); sys.path.insert(0, ROOT + r'\tools\wip\mc'); sys.path.insert(0, ROOT + r'\tools\wip\mc\s10')
import fibsim, fibwhatif, mcsim3
sys.argv, args = sys.argv[:2] + ['1', '1'], sys.argv
import ksearch4 as K4  # runs a 1-iter search at import; harmless
ev = fibsim.parse(args[1]); R0 = fibwhatif.groups(ev)
IT = int(args[2]); D = 999
def search(R, seed):
    npre = sum(len(r['order']) for r in R[:3])
    random.seed(seed); best = None; bs = (999,)
    def sc(x):
        o = [b for b in mcsim3.sim(R, K4.freqs(x)) if b != D]
        pre, inv, oo = mcsim3.score(o, npre - (1 if D in sum((r['order'] for r in R[:3]), []) else 0))
        return inv, pre, oo
    for it in range(IT):
        if best is None or random.random() < 0.02:
            x = {k: random.uniform(*v) for k, v in K4.K.items()}
        else:
            x = dict(best)
            for k in random.sample(list(K4.K), random.choice((1, 1, 2, 3))):
                lo, hi = K4.K[k]; x[k] = min(hi, max(lo, x[k] + random.gauss(0, (hi - lo) / 6)))
        inv, pre, oo = sc(x)
        if (inv, -pre) <= bs:
            bs, best = (inv, -pre), x
            if inv == 0: break
    return bs, best
base = min(search(R0, s)[0] for s in (1, 2))
print('baseline', base, flush=True)
res = []
for ri in (2, 3):   # round index 0-based: 3rd and 4th round
    r = R0[ri]
    sites = [('pre', None)] + [('g', b) for b in r['order']]
    for kind, b in sites:
        for evk in ('this', 'next') if ri == 2 else ('this',):
            for key in (0, -1, -2, -3, -4, -5, -6, -8, -1000101, -1000404, -1000707):
                R = copy.deepcopy(R0)
                e = ('ins', evk, D, key)
                (R[ri]['pre'] if kind == 'pre' else R[ri]['g'][b]).append(e)
                if ri == 2 and evk == 'this':
                    pass
                try:
                    bs = min(search(R, s)[0] for s in (1, 2))
                except Exception as ex:
                    continue
                res.append((bs, ri + 1, kind, b, evk, key))
                if bs < base: print('BETTER', bs, ri + 1, kind, b, evk, key, flush=True)
res.sort(); print(res[:10])
