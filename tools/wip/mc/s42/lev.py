"""lev.py: bcp-goto frequency levers (site line, target label line, nterms) on H5b.c; records
53/77/79 insertion signature, true inv; race-free tags. python lev.py OUT.jsonl [nterms...]"""
import sys, os, json, re, itertools, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import ev, tt, hsim
D = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\v\mc42'
BASE = open(os.environ.get('BASE', 'H5b.c')).read().split('\n')
LO, HI = 592, 724   # option loop (1-based)
def stmt_start(k):
    s = BASE[k - 1].strip()
    return s and not s.startswith(('}', 'else', '{', '#', '/')) and not re.match(r'^\w+:', s)
def site_ok(k):
    if not stmt_start(k): return False
    p = BASE[k - 2].rstrip()
    return p.endswith((';', '{', '}'))
SITES = [k for k in range(LO + 1, HI) if site_ok(k)]
TGTS = [k for k in range(int(os.environ.get("TLO", LO + 1)), int(os.environ.get("THI", HI))) if stmt_start(k)]
def sig(tag):
    R, k = hsim.load(os.path.join(D, 'slot_' + tag)); out = []
    for ri, r in enumerate(R, 1):
        for g, es in [('pre', r['pre'])] + list(r['g'].items()):
            for e in es:
                if e[0] in ('ins', 'push') and any(x in (53, 77, 79) for x in e[1:3] if isinstance(x, int)):
                    out.append('%d:%s:%s' % (ri, g, '/'.join(map(str, e[:3]))))
    return out
def make(site, tgt, nt, n0=700):
    L = list(BASE)
    L[tgt - 1] = 'zq%d: ' % tgt + L[tgt - 1]
    cond = ' && '.join('(char *)__builtin_constant_p(i + %d) == (char *)1' % (n0 + j) for j in range(nt))
    L.insert(site - 1, 'if (%s) goto zq%d;' % (cond, tgt))
    return '\n'.join(L)
def run(c):
    site, tgt, nt = c
    tag = 'l%d' % tt.tid()
    r = ev.ev(make(site, tgt, nt), tag, fncmp=False)
    if r is None: return dict(c=c, err=1)
    return dict(c=c, inv=r['tinv'], miss=r['tmiss'], sig=sig(tag), o=r['o'])
if __name__ == '__main__':
    nts = [int(x) for x in sys.argv[2:]] or [1]
    cands = [(s, t, n) for n in nts for s in SITES for t in TGTS if s != t]
    print(len(SITES), len(TGTS), len(cands), flush=True)
    done = set()
    if os.path.exists(sys.argv[1]): done = {tuple(json.loads(l)['c']) for l in open(sys.argv[1])}
    cands = [c for c in cands if c not in done]
    with open(sys.argv[1], 'a') as f, cf.ThreadPoolExecutor(4) as ex:
        for r in ex.map(run, cands):
            f.write(json.dumps(r) + '\n'); f.flush()
