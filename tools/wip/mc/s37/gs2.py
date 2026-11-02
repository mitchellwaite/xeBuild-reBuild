"""gs2.py STATE.json OUT.log ROUNDS [BEAM]: beam search (real compiles) on JMP-free-eb states.
state = {'v','a','e'}; candidates = gs.cands minus eb JMP sites + ebl bcp singles. score 10*inv + fncmp/20."""
import json, sys, os
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gs, ev, ebl
EBJ = ('elt<', 'enet<', 'eneg<', 'esucc<', 'eerase<', 'einv>', 'eout<', 'eout>', 'efail<', 'efail>', 'esucc>', 'eerase>', 'einv<')
XTG = ['u2', 'hdd4', 'hdd5', 's4', 's5', 'c12', 'c7', 'cdef', 'i1', 'p1', 'c10']
def build(st):
    import loopsites as L
    t = ebl.ebinj(gs.build(st), [tuple(x) for x in st.get('e', [])])
    for s_, tg in st.get('j', []): t = L.add(t, s_, tg)
    return t
def cands(st):
    e = st.get('e', [])
    for c in gs.cands({'v': st['v'], 'a': st['a']}):
        if c['v'] and c['v'][-1][0] in EBJ: continue
        if c['v'] and c['v'][-1][0].startswith('!ebtop'): continue
        c['e'] = e; c['j'] = st.get('j', []); yield c
    if os.environ.get('XT') == '1':
        for arm in gs.ARMORD:
            n = 500 + 10 * len(st['a'])
            for tg in XTG:
                for w in ('b', 'p', 'q', 'pp', 'qq'):
                    yield {'v': st['v'], 'a': st['a'] + [[tg, arm, w, n]], 'e': e, 'j': st.get('j', [])}
    n = 90 + 10 * len(e)
    for s in ebl.SRCS:
        for t in ebl.fwd(s):
            for w in ('b', 'p', 'q', 'pp', 'qq'):
                yield {'v': st['v'], 'a': st['a'], 'e': e + [[s, w, t, n]], 'j': st.get('j', [])}
def meas(x):
    i, st = x; import tt; tag = os.environ.get('TP', 'b') + '%d' % tt.tid()
    try: r = ev.ev(build(st), tag, fncmp=True)
    except Exception: return st, None
    if r is None: return st, None
    return st, (10 * r['score'] + r['fncmp'] / 20.0, r['score'], r['fncmp'], ' '.join(map(str, r['o'][12:])))
if __name__ == '__main__':
    beam = [json.load(open(sys.argv[1]))]; log = open(sys.argv[2], 'a'); B = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    seen = set(); best = None
    for rnd in range(int(sys.argv[3])):
        jobs = []
        for st in beam:
            for c in cands(st):
                k = json.dumps(c, sort_keys=True)
                if k not in seen: seen.add(k); jobs.append(c)
        res = []; outs = {}
        with ThreadPoolExecutor(4) as ex:
            for s, r in ex.map(meas, enumerate(jobs)):
                if r and r[3] not in outs: outs[r[3]] = 1; res.append((r, s))
        res.sort(key=lambda z: z[0][0])
        print('round', rnd, 'n', len(jobs), file=log)
        for r, s in res[:8]: print('  ', r[:3], s['v'][-1:], s['a'][-1:], s['e'][-1:], r[3][:90], file=log)
        log.flush()
        if best is None or res[0][0][0] < best[0][0]: best = res[0]; json.dump(best[1], open(sys.argv[2] + '.best.json', 'w'))
        beam = [s for r, s in res[:B]]
    print('final', best[0], json.dumps(best[1]), file=log, flush=True)
