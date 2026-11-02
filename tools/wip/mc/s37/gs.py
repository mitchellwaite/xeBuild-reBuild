"""gs.py STATE.json OUT.log ROUNDS : greedy real-compile search. state = {'v': voc design, 'a': [[label, arm, w, n]]}.
labels k55l/k61l/k67l sit before the -r/-w/-e tests; arm injections are bcp gotos (inj48.W forms).
candidates per round: every voc injection/RAW edit (single target) + every arm injection; score 10*inv + fncmp/20."""
import json, sys, os, itertools, re
os.environ['DUP'] = '1'
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voc, ev, k67, inj48
TEST = {'k49l': '} else if (!strnicmp(argv[i], "-ip", 3)) {', 'k55l': '} else if (!strnicmp(argv[i], "-r", 2)) {', 'k61l': '} else if (!strnicmp(argv[i], "-w", 2)) {',
        'k67l': '} else if (E(!strnicmp(argv[i], "-e", 2))) {'}
ARMORD = ['top', 'noent', 'rbt', 'rb', 's', 'keys', 'ip', 'r', 'w']
FWD = {'k49l': ARMORD[:6], 'k55l': ARMORD[:7], 'k61l': ARMORD[:8], 'k67l': ARMORD[:9]}
def build(st):
    t = voc.make(st['v'])
    for lb in sorted({a[0] for a in st['a'] if a[0] in TEST}):
        K = TEST[lb]; t = t.replace(K, K.replace('} else if', '} else { %s: if' % lb, 1))
        p = t.rindex('client_usage(1, argv[i]);'); t = t[:p] + 'client_usage(1, argv[i]); }' + t[p + len('client_usage(1, argv[i]);'):]
    lus = sorted({a[0] for a in st['a'] if a[0].startswith('lu')})
    if lus:
        p0 = t.index('int mode_client('); p1 = t.index('NO_MODE_ARG', p0); seg = t[p0:p1]; k = [0]
        def rep(m):
            s = ('lu%d: ' % k[0] if 'lu%d' % k[0] in lus else '') + m.group(0); k[0] += 1; return s
        seg = re.sub(r'client_usage\(\d, argv\[i\]\);', rep, seg); t = t[:p0] + seg + t[p1:]
    for lb, arm, w, n in st['a']: t = k67.inj(t, arm, w, n, lb)
    return t
def cands(st):
    for s in voc.SITES:
        if not (s.startswith('!') or s in ('elt<', 'enet<', 'eneg<', 'c6<', 'c7t<', 'c12t<')): continue
        for tg in voc.targets_for(s): yield {'v': st['v'] + [[s, [tg]]], 'a': st['a']}
    used = {(a[1], a[3]) for a in st['a']}
    for lb, arms in FWD.items():
        for arm in arms:
            n = 10 + 10 * sum(1 for a in st['a'] if a[1] == arm)
            for w in ('b', 'p', 'q', 'pp', 'qq', 'pq', 'ppp', 'pqq'):
                yield {'v': st['v'], 'a': st['a'] + [[lb, arm, w, n]]}
    if os.environ.get('LU') == '1':
        n = 10 + 10 * sum(1 for a in st['a'] if a[1] == 'top')
        for k in range(17):
            for w in ('p', 'pp', 'qq'):
                yield {'v': st['v'], 'a': st['a'] + [['lu%d' % k, 'top', w, n]]}
def meas(x):
    i, st = x; tag = 'g%d' % __import__('tt').tid()
    try: r = ev.ev(build(st), tag, fncmp=True)
    except Exception as e: return st, None
    if r is None: return st, None
    return st, (10 * r['score'] + r['fncmp'] / 20.0, r['score'], r['fncmp'], ' '.join(map(str, r['o'][12:])))
if __name__ == '__main__':
    st = json.load(open(sys.argv[1])); log = open(sys.argv[2], 'a')
    _, cur = meas((0, st)); print('start', cur, file=log, flush=True)
    for rnd in range(int(sys.argv[3])):
        res = []
        with ThreadPoolExecutor(4) as ex:
            for s, r in ex.map(meas, enumerate(cands(st))):
                if r: res.append((r, s))
        res.sort(key=lambda z: z[0][0])
        print('round', rnd, 'n', len(res), file=log)
        for r, s in res[:5]: print('  ', r[:3], s['v'][-1:], s['a'][-1:], r[3][:80], file=log)
        log.flush()
        if res[0][0][0] >= cur[0]: print('stuck', file=log); break
        cur, st = res[0]
        json.dump(st, open(sys.argv[2] + '.state.json', 'w'))
    print('final', cur, json.dumps(st), file=log, flush=True)
