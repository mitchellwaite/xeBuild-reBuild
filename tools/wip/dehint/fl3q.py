"""fl3q.py <mode> [N seed]: the nbl test (dead, no uninitialised read) at comma's site.
arms: natural arms and spellings of it, from the lean state.  sub: all subsets of the other tests at small arms (random arms if N given)."""
import itertools, random, sys, threading
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import fllib as L, fl3g as G

NB = 'nbl != 6 && nbl != 9'
SP = {'i': 'i < 0', 'nul': 'nul < -1', 'off3': 'off < -1', 'off4': 'off < -1', 'len': 'len < 0', 'x': 'off < 0', 'off5': 'off < -1'}
LEAN = dict(i=1, nul=1, off3=2, off4=1, len=1, x=2)


def state(keep, c=(NB, 1)):
    st = {n: (SP[n], k) for n, k in keep.items()}
    if c:
        st['comma'] = c
    return st


loc = threading.local()
cnt = [0]
lock = threading.Lock()


def one(kv):
    if not hasattr(loc, 'id'):
        with lock:
            cnt[0] += 1
            loc.id = cnt[0]
    n, s = kv
    o = L.compile(s, None, 'q_%d' % loc.id)
    if o is None:
        return 10**7, '', n
    return L.score(o)[0], G.vec(o), n


def run(V, name):
    with ThreadPoolExecutor(4) as ex:
        rs = sorted(ex.map(one, V.items()), key=lambda r: r[0])
    with open(L.BD + '/a3/%s.txt' % name, 'a', newline='\n') as f:
        for r in rs:
            f.write('%s\t%s\t%s\n' % r)
    print(Counter((r[0], r[1]) for r in rs if r[0] < 30).most_common(8))
    for r in rs[:14]:
        print(r)
    print('MATCH', [r[2] for r in rs if r[0] == 0][:40])


mode = sys.argv[1]
if mode == 'arms':
    CS = [NB, 'nbl != 9 && nbl != 6', 'nbl == 7', 'nbl == 8', 'nbl == 0', 'nbl != 6 && nbl < 9', 'nbl > 6 && nbl < 9', 'nbl < 6 || nbl > 9', 'nbl < 0', 'nbl > 9', 'nbl <= 0', 'nbl == 7 || nbl == 8']
    AS = [1, 2, 'nbl = 6', 'nbl = 9', 'nbl = 0', 'i = 0', 'pos = off', 'pos = size', 'off = 0', 'return 0', 'free(buf); return 0', 'log_printf(0, "x\\n"); free(buf); return 0', 'buf[pos] = 0', 'buf[off] = 0', 'buf[size] = 0', '*buf = 0', 'xb.nFiles = 0', 'xb.nFirmware = 0', 'xb.cbb = 0']
    V = {}
    for c, a in itertools.product(CS, AS):
        V['%s:%s' % (c, a)] = G.gen(state(LEAN, (c, a)))
    print(len(V))
    run(V, 'q3a')
elif mode == 'site':
    AS = ['buf[pos] = 0', 'buf[size] = 0', '*buf = 0', 'xb.cbb = 0', 'xb.nFiles = 0', 'xb.nFirmware = 0', 'xb.nFlashFiles2 = 0', 'xb.nRawPatches = 0', 'tmp[0] = 0', 'label[0] = 0', 'buf[pos] = 0; buf[size] = 0', 'xb.nFiles = 0; xb.nFirmware = 0', 'xb.cbb = 0; xb.nFiles = 0', 'buf[size] = 0; *buf = 0', 'xb.nFirmware = 0; *buf = 0', 'i = 0', 'pos = 0']
    V = {}
    for n, c, a in itertools.product(LEAN, [None, NB], AS):
        st = state(LEAN, (NB, 'xb.nFiles = 0'))
        st[n] = (c or SP[n], a)
        V['%s:%s:%s' % (n, c or SP[n], a)] = G.gen(st)
    print(len(V))
    run(V, 'q3b')
elif mode == 'sub':
    V = {}
    names = list(LEAN)
    for r in range(0, 6):
        for rm in itertools.combinations(names, r):
            k = {n: v for n, v in LEAN.items() if n not in rm}
            V['-' + '+'.join(rm)] = G.gen(state(k))
    print(len(V))
    run(V, 'q3s')
else:
    N, seed = int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    V = {}
    names = list(LEAN) + ['off5']
    while len(V) < N:
        k = {}
        for n in names:
            if rng.random() < (0.15 if n == 'off5' else 0.65):
                k[n] = LEAN.get(n, 1) if rng.random() < 0.5 else rng.randint(1, 5)
        ck = rng.randint(1, 3)
        st = state(k, (NB, ck))
        lab = ','.join('%s=%d' % kv for kv in sorted(k.items())) + '+nb=%d' % ck
        for n in k:
            if rng.random() < 0.2:
                st[n] = (NB, k[n])
                lab += '+N' + n
        V[lab] = G.gen(st)
    run(V, 'q3r')
