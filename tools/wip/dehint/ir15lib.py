"""Attempt 15 helpers.  Replace getImageSmc's whole text in the attempt 14 draft with a body, score it, write the variant.
python tools/wip/dehint/ir15lib.py <body.c> : score a file holding the function from its signature line on (loadSmc stays)."""
import difflib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

BASE = os.path.join(irlib.R, 'tools', 'wip', 'dehint', 'drafts', 'image_read_attempt14.c')
base = open(BASE, newline='').read().replace('\r\n', '\n')
A = base.index('/* One optimize attribute and the else arm')
B = base.index('void getImageKv(void)')
L0 = base.index('static void loadSmc(int addr, int size)')


def put(fn_text, loadsmc=None):
    """the draft with getImageSmc replaced; loadsmc also replaces the helper"""
    t = base[:A] + fn_text + '\n' + base[B:]
    if loadsmc is not None:
        t = t[:L0] + loadsmc + '\n' + t[A - (A - L0) + len(base[L0:A]):] if False else t[:L0] + loadsmc + '\n' + t[t.index(fn_text):]
    return t


def score(text):
    """(strict, loose, others) for _getImageSmc and the rest; ('E', msg) if it does not compile"""
    ok, o, d = irlib.compile_src(text, [])
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


def diff(text, fn='_getImageSmc'):
    ok, o, d = irlib.compile_src(text, [])
    if not ok:
        return o
    fns, _ = irlib.disasm(o)
    irlib.cleanup(d)
    a = irlib.strip_addr(irlib.ref()['fns'][fn])
    b = irlib.strip_addr(fns[fn])
    return '\n'.join(l for l in difflib.unified_diff(a, b, 'ref', 'draft', lineterm='', n=2))


if __name__ == '__main__':
    t = put(open(sys.argv[1], newline='').read().replace('\r\n', '\n'))
    print(score(t))
    if len(sys.argv) > 2:
        print(diff(t))
