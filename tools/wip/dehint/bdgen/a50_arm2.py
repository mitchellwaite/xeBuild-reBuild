"""Attempt 50: case 24's second arm through loadBl24 again (attempt 49: 25 loose with the label), on
src and with useNandData (a50_nand.py's equal base, kv and kvAlt in both loaders), in a few forms.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a50_arm2.py [-p 95,99]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub, OFF
import a50_nand as N

BASE = H.BASE
I = '\t\t\t\t'
OLDARM = I + 'if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) {\n'
LABL = I + 'devgl: __attribute__((hot));\n'
BODY = (I + '\tr = 0;\n' + I + '\tif (loadBaseFile(e->name, e))\n' + I + '\t\tr = defaultBl60(e);\n' + I +
        '\telse if (e->size != 0x60)\n' + I + '\t\tr = defaultBl60(e);\n' + I + '}\n')


def arm(form, lab):
    def f(t):
        a = t.index(OLDARM)
        b = t.index(LABL, a)
        c = t.index(BODY, b) + len(BODY)
        L = (I + '\tdevgl: __attribute__((hot));\n') if lab else ''
        if form == 'call':
            new = OLDARM + L + I + '\tr = loadBl24(e);\n' + I + '}\n'
        elif form == 'brk':
            new = I + 'if (xb.type != BUILD_DEVGL && xb.type != BUILD_DEVGL16)\n' + I + '\tbreak;\n' + \
                  (I[:-1] + 'devgl: __attribute__((hot));\n' if lab else '') + I + 'r = loadBl24(e);\n'
        elif form == 'brkw':
            new = I + 'if (xb.type != BUILD_DEVGL && xb.type != BUILD_DEVGL16)\n' + I + '\tbreak;\n' + \
                  (I[:-1] + 'devgl: __attribute__((hot));\n' if lab else '') + \
                  BODY.replace(I + '\t', I)[:-len(I + '}\n')]
        else:
            raise ValueError(form)
        return t[:a] + new + t[c:]
    return f


V = {}
for base in ('src', 'nand'):
    for form in ('call', 'brk', 'brkw'):
        for lab in (1, 0):
            for k in ('all', 'pr'):
                def g(t, base=base, form=form, lab=lab, p=OFF[k]):
                    if base == 'nand':
                        t = N.mk('ka', 'ka')(t)
                    t = arm(form, lab)(t)
                    for a, c in p:
                        t = sub(t, a, c)
                    return t
                V['%s_%s_%s_%s' % (base, form, 'L' if lab else 'n', k)] = g
