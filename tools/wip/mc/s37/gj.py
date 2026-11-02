"""gj.py STATE.json OUT.log ROUNDS [BEAM] : gs2 beam + loop-site asm-goto JMPs (state 'j': [[site, [targets]]]).
score 10*inv + fncmp/20 + 3*cm_lines (cm only for top results)."""
import json, sys, os
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gs2, ev, cm, loopsites as L
D = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\v\mc37'
LAB = ['c1','c2','c3','c7','c8','c9','c10','c11','c12','cdef','hdd4','hdd5','i0','i1','p0','p1','s4','s5','u2']
SITES = [s for s in L.LS if s != 'u0']
def build(st):
    return gs2.build(st)
    for s, tg in st.get('j', []): t = L.add(t, s, tg)
    return t
def cands(st):
    j = st.get('j', [])
    if os.environ.get('NOG') != '1':
        for c in gs2.cands({k: v for k, v in st.items() if k != 'j'}): c['j'] = j; yield c
    used = {s for s, _ in j}
    for s in SITES:
        if s in used: continue
        for t in LAB: yield dict(st, j=j + [[s, [t]]])
    for i, (s, tg) in enumerate(j):
        for t in LAB:
            if t not in tg: yield dict(st, j=j[:i] + [[s, tg + [t]]] + j[i + 1:])
def meas(x):
    i, st = x; import tt; tag = os.environ.get('TP', 'g') + '%d' % tt.tid()
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
                if r and r[3] + str(r[2]) not in outs: outs[r[3] + str(r[2])] = 1; res.append((r, s))
        res.sort(key=lambda z: z[0][0])
        # content check on top few
        top = []
        for r, s in res[:3 * B + 3]:
            p = os.path.join(D, 'v_cm.c'); open(p, 'w', newline='\n').write(build(s)); c = cm.cm(p)
            top.append(((r[0] + 3 * c[0],) + r[1:] + (c,), s))
        top.sort(key=lambda z: z[0][0])
        print('round', rnd, 'n', len(jobs), file=log)
        for r, s in top[:8]: print('  ', r[:3], r[4], s.get('j', [])[-1:], s['v'][-1:], s['a'][-1:], s['e'][-1:], r[3][:100], file=log)
        log.flush()
        if best is None or top[0][0][0] < best[0][0]: best = top[0]; json.dump(best[1], open(sys.argv[2] + '.best.json', 'w'))
        beam = [s for r, s in top[:B]]
    print('final', best[0], json.dumps(best[1]), file=log, flush=True)
