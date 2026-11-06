"""Attempt 17, pin_size: scoped and typed locals in calcBlAreaSize, pin off.  Attempt 7 found the pin is about PRE's
SSA names in the kit arm (prephitmp below the size PHI, so forwprop puts it first).  Scoped locals change which
decls and temporaries exist per arm, which earlier sweeps (types of the shared locals, declaration order,
helpers) didn't try.  Axes: x's type (findFile returns int), x declared per arm, xs declared in its block,
size's type.  Runs on src as of d09240ad."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

FN = 'uint32_t calcBlAreaSize(void)\n'


def mk(b, xt, scope, xsin, st):
    i, j = bdrun.fnspan(b, FN)
    f = b[i:j]
    f = f.replace('\t\t__asm__("" : "+b"(size));\n', '')
    f = f.replace('\t\t/* the sum so far in ebx (esi up to the 13 lookup), as in the\n\t\t   original: IRA otherwise keeps it in esi */\n', '')
    decl = '\tuint32_t size, xs, x;\n'
    assert decl in f
    parts = ['%s size' % st]
    if not xsin:
        parts.append('xs')
    d = '\t%s %s;\n' % (st, ', '.join(p.split()[-1] for p in parts))
    if not scope:
        d += '\t%s x;\n' % xt
    f = f.replace(decl, d, 1)
    if scope:
        for head in ('\tif (xb.type == BUILD_JTAG) {\n', '\t} else if (xb.type > BUILD_DEVGL16) {\n'):
            f = f.replace(head, head + '\t\t%s x;\n\n' % xt, 1)
        f = f.replace('\t\tif (xb.type != BUILD_RETAIL) {\n\t\t\tx = findFile(25);',
                      '\t\tif (xb.type != BUILD_RETAIL) {\n\t\t\t%s x = findFile(25);' % xt, 1)
    if xsin:
        f = f.replace('\t\t\t\txs = xb.files[x].size;', '\t\t\t\tuint32_t xs = xb.files[x].size;', 1)
    return b[:i] + f + b[j:]


def CASES(base):
    out = []
    for c in itertools.product(['uint32_t', 'int', 'unsigned'], [0, 1], [0, 1], ['uint32_t', 'int', 'unsigned long']):
        out.append(('x=%s scope%d xsin%d size=%s' % c, lambda b, c=c: mk(b, *c)))
    return out


FOCUS = ['_calcBlAreaSize']
