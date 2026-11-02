"""lev2.py: multi-lever builder + race-free beam on top of H5b.c.
edits = [(site, tgt, nt)]; python lev2.py SEED.json OUT.log ROUNDS BEAM"""
import sys, os, json, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lev, ev, cm, tt
def make(edits):
    L = [[x] for x in lev.BASE]   # per line: [prefix inserts..., line]
    lab = set()
    for k, (s, t, nt) in enumerate(edits):
        if t not in lab: L[t - 1][-1] = 'zq%d: ' % t + L[t - 1][-1]; lab.add(t)
        n0 = 700 + 37 * k
        cond = ' && '.join('(char *)__builtin_constant_p(i + %d) == (char *)1' % (n0 + j) for j in range(nt))
        L[s - 1].insert(0, 'if (%s) goto zq%d;' % (cond, t))
    return '\n'.join(x for l in L for x in l)
def meas(edits, full=True):
    tag = 'm%d' % tt.tid(); t = make(edits)
    r = ev.ev(t, tag, fncmp=False)
    if r is None: return None
    out = dict(e=edits, inv=r['tinv'] + 5 * len(r['tmiss']), sig=lev.sig(tag), o=r['o'])
    if full and out['inv'] <= 6:
        p = os.path.join(lev.D, 'v_%s.c' % tag); out['cm'] = cm.cm(p)
    return out
def score(r): return 10 * r['inv'] + (r['cm'][0] if 'cm' in r else 99)
if __name__ == '__main__':
    beam = [json.load(open(sys.argv[1]))]; log = open(sys.argv[2], 'a')
    NT = [int(x) for x in os.environ.get("NT", "1").split(",")]
    for rnd in range(int(sys.argv[3])):
        cands = []
        for b in beam:
            for s in lev.SITES:
                for t in lev.TGTS:
                    for nt in NT:
                        if s != t: cands.append(b + [[s, t, nt]])
        res = []
        with cf.ThreadPoolExecutor(4) as ex:
            for r in ex.map(meas, cands):
                if r is None: continue
                log.write(json.dumps(r) + '\n'); log.flush(); res.append(r)
        res.sort(key=score)
        beam = [r['e'] for r in res[:int(sys.argv[4])]]
        print('round', rnd, [(score(r), r['e'], r.get('cm')) for r in res[:5]], flush=True)
