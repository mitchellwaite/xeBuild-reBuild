"""Attempt 18, `else if (type)`: the passed log guarded by a live test of the result instead of a dead test of type.

The dead `else if (type)` is there so the passed arm's first block holds no call (no PRED_CALL against it, so the
verify-failed arm keeps its 29% from the call heuristic alone).  A result variable tested after the verify (`if
(!*pr)` or a local `ok`) does the same with a live test: *pr is 0 there unless the verify failed, and the test
threads away once *pr is known on each path.  Axes: the passed-log form, with the t5le label and the `*pr` expect
kept or not.  Runs on src as of 8b56de61."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

FAIL = '\t\t\t\t\tlog_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);\n'
PASS = '\t\t\t\t\tlog_printf(1, "loaded %s, signature check passed!\\n", e->name);\n'
OLD = ('\t\t\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n' + FAIL + '\t\t\t\t\t*pr = -1;\n'
       '\t\t\t\t/* Borderline, for review: type is 5, 11 or 17 here, so this test\n'
       '\t\t\t\t   is always true; a plain else costs 54 lines */\n'
       '\t\t\t\t} else if (type)\n' + PASS)
P4 = PASS[1:]
F = {
    'prz': ('\t\t\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n' + FAIL + '\t\t\t\t\t*pr = -1;\n\t\t\t\t}\n'
            '\t\t\t\tif (!*pr)\n' + PASS),
    'prz2': ('\t\t\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n' + FAIL + '\t\t\t\t\t*pr = -1;\n\t\t\t\t}\n'
             '\t\t\t\tif (*pr == 0)\n' + PASS),
    'prset': ('\t\t\t\t*pr = cbVerifySig(e->data, xb.pub1bl) ? 0 : -1;\n'
              '\t\t\t\tif (*pr)\n\t' + P4.replace('loaded %s, signature check passed!', 'XX') ),
    'ok': ('\t\t\t\tint ok = cbVerifySig(e->data, xb.pub1bl);\n\n'
           '\t\t\t\tif (!ok) {\n' + FAIL + '\t\t\t\t\t*pr = -1;\n\t\t\t\t}\n'
           '\t\t\t\tif (ok)\n' + PASS),
    'okelse': ('\t\t\t\tint ok = cbVerifySig(e->data, xb.pub1bl);\n\n'
               '\t\t\t\tif (!ok) {\n' + FAIL + '\t\t\t\t\t*pr = -1;\n\t\t\t\t} else if (ok)\n\t' + PASS),
    'passfirst': ('\t\t\t\tif (cbVerifySig(e->data, xb.pub1bl)) {\n\t' + PASS + '\t\t\t\t} else {\n' + FAIL +
                  '\t\t\t\t\t*pr = -1;\n\t\t\t\t}\n'),
    'prz_else': ('\t\t\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n' + FAIL + '\t\t\t\t\t*pr = -1;\n'
                 '\t\t\t\t} else if (!*pr)\n\t' + PASS),
}
del F['prset']


def mk(b, f, t5, pr):
    b = bdrun.sub(b, OLD, F[f], 1)
    offs = []
    if not t5:
        offs.append('lab_t5le')
    if not pr:
        offs.append('exp_pr')
    return bdhints.off(b, *offs)


def CASES(base):
    out = []
    for f, t5, pr in itertools.product(F, [1, 0], [1, 0]):
        out.append(('%s t5%d pr%d' % (f, t5, pr), lambda b, c=(f, t5, pr): mk(b, *c)))
    return out


FOCUS = ['_loadBlFiles']
