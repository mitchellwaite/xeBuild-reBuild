# attempt 19: pin_hdr (A). PRED_CALL cancels when both sides of the test hold a call (q.c probes: 50%), and opcode positive alone is 27%, inside (A)'s window 23..28. So `pageErased(...) > 0` or `< 1`, with the copy in both arms (memcpy is a call at estimate time).
# `IWB=build/iw/a19/t1.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw265.py -n 40 -t 1`
import os, itertools
BASE = os.environ.get('IWB', 'build/iw/a19/t1.c')
X = '(b * 32 + p) * 512'; Y = '(b * 32 + p) * 16'
TOP = '\t\t\tq = xb.spare;\n\t\t\th = xb.hdr;\n'
HEAD = 'pageErased(h + %s, q + %s)' % (X, Y)
ARM0 = '\t\t\t\tcalcPageEcc(xb.hdr + %s, xb.spare + %s);\n\t\t\t\tq = xb.spare;\n\t\t\t\th = xb.hdr;\n' % (X, Y)
C1 = '\t\t\t\tmemcpy(raw, h + %s, 512);\n' % X
C2 = '\t\t\t\tmemcpy(raw + 512, q + %s, 16);\n' % Y
TAIL1 = '\t\t\tmemcpy(raw, h + %s, 512);\n' % X
TAIL2 = '\t\t\tmemcpy(raw + 512, q + %s, 16);\n' % Y
OLD = TOP + '\t\t\tif (!' + HEAD + ') {\n' + ARM0 + '\t\t\t}\n' + TAIL1 + TAIL2
INC = '\t\t\traw += 528;\n'
F = []
def add(lab, s, extra=()):
    F.append((lab, [(OLD, s)] + list(extra)))
for tn, ecc, er in (('lt', HEAD + ' < 1', None), ('le', HEAD + ' <= 0', None), ('gt', None, HEAD + ' > 0'), ('ge', None, HEAD + ' >= 1'), ('nt', '!' + HEAD, None)):
    if ecc:
        add(tn + '_1', TOP + '\t\t\tif (' + ecc + ') {\n' + ARM0 + C1 + '\t\t\t} else\n' + C1 + TAIL2)
        add(tn + '_2', TOP + '\t\t\tif (' + ecc + ') {\n' + ARM0 + C1 + C2 + '\t\t\t} else {\n' + C1 + C2 + '\t\t\t}\n')
        add(tn + '_c', TOP + '\t\t\tif (' + ecc + ') {\n' + ARM0 + C1 + C2 + '\t\t\t\traw += 528;\n\t\t\t\tcontinue;\n\t\t\t}\n' + TAIL1 + TAIL2)
    else:
        add(tn + '_1', TOP + '\t\t\tif (' + er + ')\n' + C1 + '\t\t\telse {\n' + ARM0 + C1 + '\t\t\t}\n' + TAIL2)
        add(tn + '_2', TOP + '\t\t\tif (' + er + ') {\n' + C1 + C2 + '\t\t\t} else {\n' + ARM0 + C1 + C2 + '\t\t\t}\n')
        add(tn + '_c', TOP + '\t\t\tif (' + er + ') {\n' + C1 + C2 + '\t\t\t\traw += 528;\n\t\t\t\tcontinue;\n\t\t\t}\n' + ARM0.replace('\t\t\t\t', '\t\t\t') + TAIL1 + TAIL2)
AXES = [F]
