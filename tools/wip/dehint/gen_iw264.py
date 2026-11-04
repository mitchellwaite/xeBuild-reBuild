# attempt 19: pin_hdr (A). t1's page body with P(ECC) moved by source shape: test spellings, goto, helpers with returns. Wanted IDENTICAL (P(ECC) 23..28%).
# `IWB=build/iw/a19/t1.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw264.py -n 40 -t 4`
import os
BASE = os.environ.get('IWB', 'build/iw/a19/t1.c')
X = '(b * 32 + p) * 512'; Y = '(b * 32 + p) * 16'
TOP = '''			q = xb.spare;
			h = xb.hdr;
'''
HEAD = 'pageErased(h + %s, q + %s)' % (X, Y)
ARM = '''				calcPageEcc(xb.hdr + %s, xb.spare + %s);
				q = xb.spare;
				h = xb.hdr;
''' % (X, Y)
TAIL = '''			memcpy(raw, h + %s, 512);
			memcpy(raw + 512, q + %s, 16);
''' % (X, Y)
OLD = TOP + '\t\t\tif (!' + HEAD + ') {\n' + ARM + '\t\t\t}\n' + TAIL
FN = 'int finalizeImage(void)\n'
def body(s): return [(OLD, s)]
L = 'copy%d'
F = [('', [])]
tests = {'ne1': HEAD + ' != 1', 'lt1': HEAD + ' < 1', 'le0': HEAD + ' <= 0', 'eq0': HEAD + ' == 0', 'ge': '1 > ' + HEAD}
for k, c in tests.items():
    F.append((k, body(TOP + '\t\t\tif (' + c + ') {\n' + ARM + '\t\t\t}\n' + TAIL)))
    F.append((k + 'g', body(TOP + '\t\t\tif (' + c + ') {\n' + ARM + '\t\t\t\tgoto copy;\n\t\t\t}\ncopy:\n' + TAIL)))
F.append(('notg', body(TOP + '\t\t\tif (!' + HEAD + ') {\n' + ARM + '\t\t\t\tgoto copy;\n\t\t\t}\ncopy:\n' + TAIL)))
F.append(('invg', body(TOP + '\t\t\tif (' + HEAD + ')\n\t\t\t\tgoto copy;\n' + ARM.replace('\t\t\t\t', '\t\t\t') + 'copy:\n' + TAIL)))
F.append(('eq1g', body(TOP + '\t\t\tif (' + HEAD + ' == 1)\n\t\t\t\tgoto copy;\n' + ARM.replace('\t\t\t\t', '\t\t\t') + 'copy:\n' + TAIL)))
F.append(('elsee', body(TOP + '\t\t\tif (' + HEAD + ') {\n\t\t\t} else {\n' + ARM + '\t\t\t}\n' + TAIL)))
F.append(('er', [(OLD, TOP + '\t\t\ter = ' + HEAD + ';\n\t\t\tif (!er) {\n' + ARM + '\t\t\t}\n' + TAIL), ('	uint8_t *h;\n', '	uint8_t *h;\n	int er;\n')]))
F.append(('sw', body(TOP + '\t\t\tswitch (' + HEAD + ') {\n\t\t\tcase 0:\n' + ARM + '\t\t\t}\n' + TAIL)))
F.append(('wh', body(TOP + '\t\t\twhile (!' + HEAD + ') {\n' + ARM + '\t\t\t\tbreak;\n\t\t\t}\n' + TAIL)))
# helpers: the arm in a static function with returns
HB = {'r0': 'static void fixPage(uint8_t *d, uint8_t *s)\n{\n\tif (pageErased(d, s))\n\t\treturn;\n\tcalcPageEcc(d, s);\n}\n\n',
      'r1': 'static void fixPage(uint8_t *d, uint8_t *s)\n{\n\tif (!pageErased(d, s)) {\n\t\tcalcPageEcc(d, s);\n\t\treturn;\n\t}\n}\n\n',
      'r2': 'static int fixPage(uint8_t *d, uint8_t *s)\n{\n\tif (pageErased(d, s))\n\t\treturn 0;\n\tcalcPageEcc(d, s);\n\treturn 1;\n}\n\n',
      'r3': 'static int fixPage(uint8_t *d, uint8_t *s)\n{\n\tif (!pageErased(d, s)) {\n\t\tcalcPageEcc(d, s);\n\t\treturn 1;\n\t}\n\treturn 0;\n}\n\n'}
for k, h in HB.items():
    F.append((k, [(OLD, TOP + '\t\t\tfixPage(h + %s, (uint8_t *)q + %s);\n\t\t\tq = xb.spare;\n\t\t\th = xb.hdr;\n' % (X, Y) + TAIL), (FN, h + FN)]))
    F.append((k + 'i', [(OLD, TOP + '\t\t\tif (fixPage(h + %s, (uint8_t *)q + %s)) {\n\t\t\t\tq = xb.spare;\n\t\t\t\th = xb.hdr;\n\t\t\t}\n' % (X, Y) + TAIL), (FN, h + FN)]))
AXES = [F]
FILTER = lambda c: not (c[0][0] in ('r0i', 'r1i'))
