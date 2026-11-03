"""python tools/wip/dehint/iwanneal2.py <seconds> <seed> [fixed tricks, comma separated]

Attempt 2's search: iwanneal's coordinate search, on drafts/image_write.c (dead tests merged, abort in imgAddFile), with the
new base's trick names: opt, pin_t, a1, a2, c3, c4, c34, a5, a6, len (`c` drops the abort test).  A fixed trick stays removed.
Objective: lines + PEN * tricks kept.  IDENTICAL variants go to build/iw/a2/an2_<kept>_<seed>.c, log build/iw/a2/an2_<seed>.log."""
import json, os, random, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
argv = sys.argv
sys.argv = ['x']
import iwanneal as A, iwlib, iwtricks
sys.argv = argv

if os.environ.get('IWDRAFT'):  # other base than drafts/image_write.c
    A.BASE = open(os.environ['IWDRAFT'], newline='').read().replace('\r\n', '\n')
M = '		if (x + 0x4000 < first || (len & 0x3fff) > 0x3fff)\n			blocks++;\n'
T2 = {
    'a1': [('	if (x > first + 0x4000)\n		blocks += 2;\n', '')],
    'a2': [('		if (x > first + 0x4000)\n			__asm__("");\n', '')],
    'c34': [(M, '')],
    'c3': [(M, '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n')],
    'c4': [(M, '		if (x + 0x4000 < first)\n			blocks++;\n')],
    'a5': [('			if (x > first + 0x4000)\n				blocks++;\n', '')],
    'a6': [('		if (x + 0x4000 < first)\n			start++;\n', '')],
    'len': [('	if ((len & 0x3fff) > 0x3fff)\n		len++;\n', '')],
    'c': [('		if ((len & 0x3fff) > 0x3fff)\n			abort();\n', '')],
}
iwtricks.T.update(T2)
TRICKS = ['opt', 'pin_t', 'a1', 'a2', 'c34', 'c3', 'c4', 'a5', 'a6', 'len', 'c']
ORDER = {'c34': 0, 'c3': 1, 'c4': 2}
A.TRICKS[:] = TRICKS
R = lambda old, *news: (old, list(news))
A.SHAPES.update({
    'fend': R('	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n',
              '	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n	uint32_t end = off + len;\n'),
    'lentest': R('	if ((len & 0x3fff) > 0x3fff)\n		len++;\n', '	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n'),
    'abtest': R('		if ((len & 0x3fff) > 0x3fff)\n			abort();\n', '		if ((end & 0x3fff) > 0x3fff)\n			abort();\n'),
    'a1body': R('	if (x > first + 0x4000)\n		blocks += 2;\n', '	if (x > first + 0x4000)\n		blocks++;\n'),
    'a5body': R('			if (x > first + 0x4000)\n				blocks++;\n', '			if (x > first + 0x4000)\n				blocks += 2;\n'),
})


def render(st):
    t = A.BASE
    gone = sorted([n for n in TRICKS if st.get(n)], key=lambda n: ORDER.get(n, 5))
    t = iwtricks.apply(t, gone)
    if ((st.get('lentest') or st.get('abtest')) and not st.get('fend')):
        st = dict(st, fend=1)
    for k, (old, news) in A.SHAPES.items():
        v = st.get(k, 0)
        if v and old in t:
            t = t.replace(old, news[v - 1])
    return t


def kept(st):
    n = 9  # param, pin_hdr, xmalloc, 2 expect, lnp2, + a1 a2 ... counted below
    n = 6 + sum(1 for x in ('opt', 'pin_t', 'a1', 'a2', 'a5', 'a6', 'len', 'c') if not st.get(x))
    if not st.get('c34') and not (st.get('c3') and st.get('c4')):
        n += 1
    return n


def score(st):
    r = iwlib.score_text(render(st), A.FLAGS)
    if 'compile' in r:
        return 10 ** 7, r
    return r['total'] + PEN * kept(st), r


PEN = 8


def main():
    secs, seed = int(sys.argv[1]), int(sys.argv[2])
    fixed = [x for x in (sys.argv[3] if len(sys.argv) > 3 else '').split(',') if x]
    rnd = random.Random(seed)
    outd = os.path.join(iwlib.BUILD, 'a2')
    log = open(os.path.join(outd, 'an2_%d.log' % seed), 'a', newline='\n')
    st = {k: True for k in fixed}
    cur, (curv, r) = st, score(st)
    print('start', curv, iwlib.fmt(r)[:200], file=log, flush=True)
    gbest, gval = cur, curv
    keys = [k for k in TRICKS + list(A.SHAPES) if k not in fixed]
    best_kept = 99
    t0 = time.time()
    seen = 0
    with ThreadPoolExecutor(4) as ex:
        while time.time() - t0 < secs:
            cands = []
            for _ in range(8):
                s = dict(cur)
                for key in rnd.sample(keys, rnd.choice((1, 1, 2, 2, 3))):
                    if key in TRICKS:
                        s[key] = not s.get(key)
                    else:
                        n = len(A.SHAPES[key][1]) + 1
                        s[key] = (s.get(key, 0) + rnd.randrange(1, n)) % n
                cands.append(s)
            res = list(ex.map(lambda s: (s, score(s)), cands))
            seen += len(cands)
            for s, (v, r) in res:
                if r.get('identical') and kept(s) < best_kept:
                    best_kept = kept(s)
                    open(os.path.join(outd, 'an2_%d_%d.c' % (best_kept, seed)), 'w', newline='\n').write(render(s))
                    print('IDENTICAL kept', best_kept, json.dumps({k: x for k, x in s.items() if x}), file=log, flush=True)
            s, (v, r) = min(res, key=lambda x: x[1][0])
            if v < gval:
                gbest, gval = s, v
                print(seen, 'best', v, 'kept', kept(s), json.dumps({k: x for k, x in s.items() if x}), iwlib.fmt(r)[:200], file=log, flush=True)
            if v <= curv or rnd.random() < 2.718 ** (-(v - curv) / 10.0):
                cur, curv = s, v
            if rnd.random() < 0.02:
                cur, curv = gbest, gval
    print('end', seen, gval, file=log, flush=True)


main()
