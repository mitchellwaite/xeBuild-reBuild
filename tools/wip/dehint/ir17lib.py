"""Attempt 17 helpers.  Replace getImageSmc (from the comment above it to getImageKv) in src/image_read.c, score strict and loose.
python tools/wip/dehint/ir17lib.py <body.c> [flags...] : score one body and print the loose diff."""
import difflib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

base = open(irlib.SRC, newline='').read().replace('\r\n', '\n')
A = base.rindex('/*', 0, base.index('void getImageSmc(void)'))  # the comment above it
B = base.index('void getImageKv(void)')
L0 = base.index('static void loadSmc(int addr, int size)')

LOG0 = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n'
L38 = 'size = 0x3800;\nlog_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
L30 = 'size = 0x3000;\nlog_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
NOTSANE = 'log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n'
HEAD = 'struct flashhdr *h = (struct flashhdr *)xb.dump;\nint addr = SWAP32(h->smcBootAddr);\nint size = SWAP32(h->smcBootSize);\n'
ATTR = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) '
LIM = '528 * xb.dumpPages'


def put(fn_text):
    return base[:A] + fn_text + '\n' + base[B:]


def score(text, flags=()):
    """(strict, loose, others, notes); ('E', msg) if it does not compile"""
    ok, o, d = irlib.compile_src(text, list(flags))
    if not ok:
        return ('E', o[:300])
    try:
        b = open(o, 'rb').read()
        r = irlib.ref()
        if b == r['bytes']:
            return (0, 0, {}, [])
        fns, order = irlib.disasm(o)
        res = {}
        for loose in (0, 1):
            if loose:
                os.environ['IRLOOSE'] = '1'
            else:
                os.environ.pop('IRLOOSE', None)
            res[loose] = irlib.fdiff(r['fns']['_getImageSmc'], fns['_getImageSmc'])
        os.environ.pop('IRLOOSE', None)
        other = {n: irlib.fdiff(r['fns'][n], fns[n]) for n in r['order'] if n != '_getImageSmc' and n in fns}
        other = {k: v for k, v in other.items() if v}
        notes = [s for s in ('.rdata', '.data', '.bss') if irlib.section(o, s) != r['sec'][s]]
        return (res[0], res[1], other, notes)
    finally:
        irlib.cleanup(d)


def diff(text, flags=(), fn='_getImageSmc'):
    ok, o, d = irlib.compile_src(text, list(flags))
    if not ok:
        return o
    fns, _ = irlib.disasm(o)
    irlib.cleanup(d)
    os.environ['IRLOOSE'] = '1'
    a = irlib.strip_addr(irlib.ref()['fns'][fn])
    b = irlib.strip_addr(fns[fn])
    os.environ.pop('IRLOOSE', None)
    return '\n'.join(l for l in difflib.unified_diff(a, b, 'ref', 'draft', lineterm='', n=1))


def sweep(forms, flagsets=(('', ()),), top=40):
    """forms {name: fn text}; prints sorted by loose"""
    res = []
    for k, t in forms.items():
        tx = put(t)
        for fk, fl in flagsets:
            s = score(tx, fl)
            if s[0] == 'E':
                print(k, fk, 'ERR', s[1][:200])
                continue
            res.append((s[1], s[0], k + fk, s[2], s[3]))
    res.sort(key=lambda x: (x[0], x[1]))
    for r in res[:top]:
        print(r)
    return res


if __name__ == '__main__':
    t = put(open(sys.argv[1], newline='').read().replace('\r\n', '\n'))
    fl = sys.argv[2:]
    print(score(t, fl))
    print(diff(t, fl))
