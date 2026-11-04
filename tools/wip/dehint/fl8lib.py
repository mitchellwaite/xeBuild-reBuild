"""fl8lib: attempt 8's type axes.  Base is src/filelist_ini.c via fl6lib (drops T1 T2 T3 KF).

A state label is `drops|axis=value,axis=value`.  Axes are in E: {axis: {value: fn(s)->s}}; add to E from a script.
Types: t.<var>=<type> for parseIni's locals.  Multi-word types use _ (`unsigned_long`).
run(V, name): score {label: source} with WORKERS threads, log to build/filelist_ini/a8/<name>.txt
"""
import itertools, os, random, re, sys, threading
from concurrent.futures import ThreadPoolExecutor
import fllib as L, fl6lib as F

A8 = os.path.join(L.BD, 'a8')
os.makedirs(A8, exist_ok=True)
S0 = F.S0
WORKERS = int(os.environ.get('WORKERS', '6'))
SUBS = ['', 'T1', 'T2', 'T3', 'T1,T2', 'T1,T3', 'T2,T3', 'T1,T2,T3']
SUBSK = SUBS + [x + ',KF' if x else 'KF' for x in SUBS]

DECL = ("\tunsigned char *buf, *p;\n"
        "\tint size, off, end, pos, len, nul, comma, n, i, nbl;\n"
        "\tuint32_t noCrc;\n\tchar *s;\n\tuint32_t crc;\n\tchar label[50];\n\tchar tmp[0x400];\n")
assert S0.count(DECL) == 1
VARS = ['size', 'off', 'end', 'pos', 'len', 'nul', 'comma', 'n', 'i', 'nbl', 'noCrc', 'crc']
DEF = {v: 'int' for v in VARS}
DEF.update(noCrc='uint32_t', crc='uint32_t')
FFSIG = "static void findField(unsigned char *p, int rem, int *comma, int *nul)"
assert S0.count(FFSIG) == 1


def types(s, t):
    """t: {var: type}, types with _ for spaces; also 'tmp', 'label' (unsigned char), 's' (char pointer kind)."""
    ty = dict(DEF)
    ty.update({k: v.replace('_', ' ') if v.startswith(('unsigned', 'long')) else v for k, v in t.items() if k in DEF})
    g = {}
    for v in VARS:
        g.setdefault(ty[v], []).append(v)
    d = "\tunsigned char *buf, *p;\n"
    for k, vs in g.items():
        d += "\t%s %s;\n" % (k, ', '.join(vs))
    d += "\t%s *s;\n" % t.get('s', 'char').replace('_', ' ')
    d += "\t%s label[50];\n\t%s tmp[0x400];\n" % (t.get('label', 'char').replace('_', ' '), t.get('tmp', 'char').replace('_', ' '))
    s = L.sub(s, DECL, d)
    if ty['comma'] != 'int' or ty['nul'] != 'int':
        s = L.sub(s, FFSIG, "static void findField(unsigned char *p, int rem, %s *comma, %s *nul)" % (ty['comma'], ty['nul']))
    return s


E = {}


def state(lb):
    d, _, a = lb.partition('|')
    s = F.drop(S0, [x for x in d.split(',') if x])
    t = {}
    rest = []
    for kv in a.split(','):
        if not kv:
            continue
        k, v = kv.split('=')
        if k.startswith('t.'):
            t[k[2:]] = v
        else:
            rest.append((k, v))
    for k, v in rest:
        s = E[k][v](s)
    if t:
        s = types(s, t)
    return s


_loc = threading.local()
_cnt = [0]
_lock = threading.Lock()


def one(kv):
    if not hasattr(_loc, 'id'):
        with _lock:
            _cnt[0] += 1
            _loc.id = _cnt[0]
    n, s = kv
    o = L.compile(s, None, 'a8_%d_%d' % (os.getpid(), _loc.id))
    if o is None:
        return 10**7, {}, [], n
    sc = L.score(o)
    return F.nscore(o, sc), sc[2], sc[3], n


def run(V, name, show=25):
    with ThreadPoolExecutor(WORKERS) as ex:
        rs = sorted(ex.map(one, V.items()), key=lambda r: r[0])
    with open(os.path.join(A8, name + '.txt'), 'a', newline='\n') as f:
        for r in rs:
            f.write('%s\t%s\t%s\t%s\n' % r)
    for r in rs[:show]:
        print(r)
    print('MATCH', [r[3] for r in rs if r[0] == 0][:40])
    return rs


def floors(rs):
    """best score per drop subset"""
    b = {}
    for r in rs:
        d = r[3].partition('|')[0]
        if d not in b or r[0] < b[d][0]:
            b[d] = (r[0], r[3])
    for k in sorted(b, key=lambda k: (len(k), k)):
        print('%-14s %s  %s' % (k or '(none)', b[k][0], b[k][1]))


def show(lb_or_src, tag='a8show'):
    import difflib
    s = state(lb_or_src) if '|' in lb_or_src or not lb_or_src else lb_or_src
    o = L.compile(s, None, tag)
    print('==', F.nscore(o), L.score(o)[2:])
    A, B = F.norm(L.dis(L.REF)), F.norm(L.dis(o))
    for k in A:
        if A[k] != B.get(k):
            print('--', k)
            print('\n'.join(l for l in difflib.unified_diff(A[k], B.get(k, []), lineterm='', n=1) if not l.startswith(('---', '+++'))))


if __name__ == '__main__':
    for lb in sys.argv[1:]:
        show(lb)
