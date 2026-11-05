"""Measurement only, getImageSmc: __builtin_expect on each test (none, 1 or 0) at several builtin-expect-probability values.  What probabilities does the natural form need?
python tools/wip/dehint/gen_ir81.py [form] : prints the best combinations, loose scores."""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor
os.environ['IRLOOSE'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib
import gen_ir80 as g

src = open(os.path.join(irlib.R, 'src', 'image_read.c'), newline='').read().replace('\r\n', '\n')
BAD, S800, S000, TAIL, NS = g.BAD, g.S800, g.S000, g.TAIL, g.NS


def X(c, k):
    return c if k == 'n' else '__builtin_expect(%s, %s)' % (c, k)


def mk(k, b_form):
    z, b, s, a8, l = k
    if b_form == 'one':
        A = f'if (!addr) {{\n{BAD}}}\nif ({X("addr != 0x800 && addr != 0x1000", b)}) {{\n{BAD}}}\n'
    else:
        A = f'if ({X("!addr", z)}) {{\n{BAD}}} else if ({X("addr != 0x800 && addr != 0x1000", b)}) {{\n{BAD}}}\n'
    if z != 'n' and b_form == 'one':
        A = f'if ({X("!addr", z)}) {{\n{BAD}}}\nif ({X("addr != 0x800 && addr != 0x1000", b)}) {{\n{BAD}}}\n'
    B = f'if ({X("size != 0x3000 && size != 0x3800", s)}) {{\nif ({X("addr == 0x800", a8)}) {{\n{S800}}} else {{\n{S000}}}\n}}\n'
    C = f'if ({X("addr < 528 * xb.dumpPages", l)}) {{\n{TAIL}}} else {{\n{NS}}}\n'
    body = 'void getImageSmc(void)\n{\n	struct flashhdr *h = (struct flashhdr *)xb.dump;\n	' + g.D['ii'] + '\n	' + A + B + C + '}\n'
    return src.replace(g.OLD, body)


def run(a):
    p, k, form = a
    r = irlib.score_text(mk(k, form), ['--param', 'builtin-expect-probability=%d' % p])
    return r.get('per', {}).get('_getImageSmc', 0 if r.get('identical') else 9999), r.get('total', 0 if r.get('identical') else 9999), p, k, form


if __name__ == '__main__':
    forms = sys.argv[1:] or ['one']
    args = [(p, k, f) for p in (55, 65, 80, 95) for k in itertools.product('n01', repeat=5) for f in forms]
    print(len(args), flush=True)
    with ThreadPoolExecutor(4) as ex:
        res = sorted(ex.map(run, args), key=lambda x: x[:2])
    for x in res[:40]:
        print(x)
