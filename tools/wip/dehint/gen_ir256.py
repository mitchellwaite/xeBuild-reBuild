"""Attempt 21: the fallback's spelling on the current layout (gen_ir248 k3, `l_early`), with and without E's statement.
F: how 0x1000 reaches addr on the zero and bad paths.  E: what the size-ok block holds."""
import itertools, multiprocessing, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import put, score, diff, LOG0, L38, L30, NOTSANE, HEAD, LIM

EXC = 'int excess = (size & ~0x800u) - 0x3000; addr += excess;'
E = {
    'none': ';',
    'exc': EXC,
    'ta': 'unsigned ta = addr; addr = ta;',
    'blk': '{ int sz = size; size = sz; }',
    'adr': 'int tmp = addr; addr = tmp;',
}
F = {
    # both arms assign (the source today)
    'two': (f'if (ok <= 0) {{ {LOG0} addr = 0x1000; }}', f'badAddr: {LOG0} addr = 0x1000; goto fixSize;'),
    # one assignment: the zero arm jumps to the bad log's assignment
    'fb': (f'if (ok <= 0) {{ {LOG0} goto fallback; }}', f'badAddr: {LOG0} fallback: addr = 0x1000; goto fixSize;'),
    # a shared block after both logs, written last of the three
    'fb2': (f'if (ok <= 0) {{ {LOG0} goto fallback; }}', f'badAddr: {LOG0} goto fallback; fallback: addr = 0x1000; goto fixSize;'),
    # the fallback through a variable: const local, static const
    'loc': (f'if (ok <= 0) {{ {LOG0} addr = dflt; }}', f'badAddr: {LOG0} addr = dflt; goto fixSize;'),
    'sta': (f'if (ok <= 0) {{ {LOG0} addr = sdflt; }}', f'badAddr: {LOG0} addr = sdflt; goto fixSize;'),
}
Tst = {
    't': 't = addr; if (t != 0x1000) { if (t != 0x800) goto badAddr; }',
    'and': 'if (addr != 0x1000 && addr != 0x800) goto badAddr;',
}


def text(f, e, tt):
    z, b = F[f]
    return f'''static const int sdflt = 0x1000;
void getImageSmc(void)
{{
{HEAD} int ok = addr != 0;
 unsigned t, lim;
 int dflt = 0x1000;
 int bad, o, out;
 (void)t; (void)dflt;
 {z}
 {Tst[tt]}
fixSize:
 bad = size != 0x3000 && size != 0x3800;
 if (bad <= 0) goto sizeOk;
 o = addr != 0x800;
 if (o > 0) goto use3000;
 {L38}
 goto check;
 {b}
use3000:
 {L30}
check:
 lim = {LIM};
 if ((unsigned)addr != lim) {{ out = (unsigned)addr >= lim; if (out <= 0) {{ loadSmc(addr, size); return; }} }}
 {NOTSANE} return;
sizeOk:
 {{ {E[e]} }}
 goto check;
}}'''


def one(k):
    return ('.'.join(k), score(put(text(*k))))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(diff(put(text(*sys.argv[1].split('.')))))
        sys.exit()
    keys = list(itertools.product(F, E, Tst))
    with multiprocessing.Pool(2) as p:
        res = p.map(one, keys, 4)
    res.sort(key=lambda x: (x[1][1] if x[1][0] != 'E' else 9999))
    for k, r in res:
        print(k, r[:2] if r[0] != 'E' else r, r[3] if r[0] != 'E' else '')
