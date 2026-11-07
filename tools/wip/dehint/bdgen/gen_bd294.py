"""Attempt 18, t5le through the signature-failed share S of the tail's flow (see "t5le and exp_pr: the joiner
arithmetic"): with the `*pr` expect kept, t5le lands if S / Xc >= 21.6% (src 15.6%), but doubling S moves the failed
log.  Natural forms of the signature block that move S by less: the order of the three types in the `||`, the
pub1bl test's polarity, the verify test's polarity, and `else if (type)` or a plain else.  Axes as listed, t5le off,
everything else as src.  Runs on src as of 8b56de61."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

FAIL = '\t\t\t\t\tlog_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);\n'
PASS = '\t\t\t\t\tlog_printf(1, "loaded %s, signature check passed!\\n", e->name);\n'
NOKEY = '\t\t\t\tlog_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);\n'
OLD = ('\t\tif (type == 5 || type == 17 || type == 11) {\n'
       '\t\t\tif (xb.pub1bl) {\n'
       '\t\t\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n' + FAIL + '\t\t\t\t\t*pr = -1;\n'
       '\t\t\t\t/* Borderline, for review: type is 5, 11 or 17 here, so this test\n'
       '\t\t\t\t   is always true; a plain else costs 54 lines */\n'
       '\t\t\t\t} else if (type)\n' + PASS +
       '\t\t\t} else\n' + NOKEY +
       '\t\t}\n')


def verify(vpol, dead):
    g = 'else if (type)\n' if dead else 'else\n'
    if vpol == 'neg':
        return ('\t\t\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n' + FAIL + '\t\t\t\t\t*pr = -1;\n'
                '\t\t\t\t} ' + g + PASS)
    if dead:
        return ('\t\t\t\tif (cbVerifySig(e->data, xb.pub1bl)) {\n\t\t\t\t\tif (type)\n\t' + PASS +
                '\t\t\t\t} else {\n' + FAIL + '\t\t\t\t\t*pr = -1;\n\t\t\t\t}\n')
    return ('\t\t\t\tif (cbVerifySig(e->data, xb.pub1bl))\n' + PASS +
            '\t\t\t\telse {\n' + FAIL + '\t\t\t\t\t*pr = -1;\n\t\t\t\t}\n')


def mk(b, order, kpol, vpol, dead):
    head = '\t\tif (' + ' || '.join('type == %d' % t for t in order) + ') {\n'
    v = verify(vpol, dead)
    if kpol == 'pos':
        body = '\t\t\tif (xb.pub1bl) {\n' + v + '\t\t\t} else\n' + NOKEY
    else:
        body = '\t\t\tif (!xb.pub1bl)\n\t' + NOKEY + '\t\t\telse {\n' + v + '\t\t\t}\n'
    b = bdrun.sub(b, OLD, head + body + '\t\t}\n', 1)
    return bdhints.off(b, 'lab_t5le')


def CASES(base):
    out = []
    for order, kpol, vpol, dead in itertools.product(itertools.permutations((5, 17, 11)), ['pos', 'neg'], ['neg', 'pos'], [1, 0]):
        out.append(('%s k%s v%s dead%d' % (''.join('%d,' % t for t in order), kpol, vpol, dead),
                    lambda b, c=(order, kpol, vpol, dead): mk(b, *c)))
    return out


FOCUS = ['_loadBlFiles']
