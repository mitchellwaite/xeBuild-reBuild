"""Attempt 19: natural spellings of the signature-failed arm that leave the profile alone but may change vrp1's copies:
the -1 stored before the log, the verify result in a local (`ok`, `sig`), declared at the top or in the block.  Each
with t5le on and off.  Runs on src as of 9210177c."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

FAIL = '\t\t\t\t\tlog_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);\n'
VER = '\t\t\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n'
KEY = '\t\t\tif (xb.pub1bl) {\n'


def mk(b, order, var, t5):
    if order == 'store_first':
        b = bdrun.sub(b, VER + FAIL + '\t\t\t\t\t*pr = -1;\n', VER + '\t\t\t\t\t*pr = -1;\n' + FAIL)
    if var == 'blk':
        b = bdrun.sub(b, KEY + VER, KEY + '\t\t\t\tint ok = cbVerifySig(e->data, xb.pub1bl);\n\n\t\t\t\tif (!ok) {\n')
    elif var == 'top':
        b = bdrun.sub(b, KEY + VER, KEY + '\t\t\t\tok = cbVerifySig(e->data, xb.pub1bl);\n\t\t\t\tif (!ok) {\n')
        b = bdrun.sub(b, 'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)\n{\n\tint type;\n',
                      'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)\n{\n\tint type, ok;\n')
    elif var == 'pr':
        # the verify result goes through *pr: 0 or -1, then the logs test it
        return None
    if not t5:
        b = bdhints.off(b, 'lab_t5le')
    return b


def CASES(base):
    out = []
    for order, var, t5 in itertools.product(['src', 'store_first'], ['none', 'blk', 'top'], [1, 0]):
        if order == 'src' and var == 'none':
            continue
        out.append(('%s %s t5le%d' % (order, var, t5), lambda b, c=(order, var, t5): mk(b, *c)))
    return out


FOCUS = ['_loadBlFiles']
