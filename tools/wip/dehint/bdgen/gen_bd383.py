"""Attempt 27: gen_bd382 found that with exp_t10 off a heavier __builtin_constant_p entry (`pi it` or `ii pt`, one
pointer compare and one int compare) puts the type-11 block back (bbro 24 at 30, against 18), leaving 2 loose lines in
loadBlFiles: bbro copies the `if (r)` test into the merged checkBl call block (116 at 99, duplication threshold
882 / 10 = 88; 73 with the expect).  116 is the type-9 checkBl path (70) plus CG's success flow (29), so CG's success
flow has to come down to 17.  Cross gen_bd381's CG arm forms (own checkBl call: PRED_CALL on the success edge; nogo;
nested) with the weights.  Runs on src as of 7a9a2b41, on gen_bd380.c2base."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bd381 as g381, gen_bd382 as g382

W = {'pp': ('pi', 'pt'), 'pi': ('pi', 'it'), 'ip': ('ii', 'pt'), 'ii': ('ii', 'it'), 'bp': ('bi', 'pt'), 'pb': ('pi', 'bt')}


def mk(b, form, w):
    b = g381.mk(b, form, 'plain')
    a, c = W[w]
    return bdrun.sub(b, g382.CP_SRC, '%s && %s' % (g382.I[a], g382.T[c]), 1)


def CASES(base):
    forms = [f for f in g381.FORMS if f != 'base'] + ['plain']
    out = []
    for f, w in itertools.product(forms, W):
        if f == 'plain':
            out.append(('plain %s' % w, lambda b, w=w: bdrun.sub(bdhints.off(g381.g380.c2base(b), 'exp_t10'), g382.CP_SRC,
                                                                '%s && %s' % (g382.I[W[w][0]], g382.T[W[w][1]]), 1)))
        else:
            out.append(('%s %s' % (f, w), lambda b, a=(f, w): mk(b, *a)))
    return out


FOCUS = ['_loadBlFiles']
