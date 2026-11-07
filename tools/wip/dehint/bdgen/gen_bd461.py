"""Attempt 34, diagnostics only (expects are tricks): does the pop order follow the frequencies (gen_bd460's theory)?
pin_d off; an expect on the d test or on the first load's failure."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdhints, bdrun

FOCUS = ['_loadBlFiles']
D = '\t\t\tif (d)\n\t\t\t\t*pr = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);'
L1 = '\t\tif (loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) &&\n'


def CASES(base):
    b0 = bdhints.off(base, 'pin_d')
    out = []
    for v in (0, 1):
        out.append(('d expect %d' % v, bdrun.sub(b0, D, D.replace('if (d)', 'if (__builtin_expect(d != 0, %d))' % v))))
        out.append(('l1 expect %d' % v, bdrun.sub(b0, L1, L1.replace('if (loadBaseFile(e->name, &xb.files[xb.nFlashFiles])',
                                                                    'if (__builtin_expect(loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) != 0, %d)' % v))))
    return out
