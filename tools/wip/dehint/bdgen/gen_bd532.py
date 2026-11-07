"""Attempt 41, lab_none: defaultBl60 written out in loadConsoleBlFiles' case 24 (loadBl keeps the helper), so the
malloc test is predicted in loadConsoleBlFiles' own profile (pointer heuristic, no early return of a helper) instead
of the late-inlined defaultBl60.isra.0's 10.1%; the r = 1 block needs 21 against the not-entered return's 20.
Two copies (if / else if) or one under `||`, failure first or success first; the precheck + label kept or gone.
Run: python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd532.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
from gen_bd530 import PRECHECK, TAIL

FOCUS = ['_loadConsoleBlFiles']
C24 = '''				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;
'''
BODY_F = '''{
					e->data = malloc(0x60);
					if (!e->data) {
						r = 1;
						break;
					}
					e->size = 0x60;
					memcpy(e->data, defBl60, 0x60);
				}'''
BODY_S = '''{
					e->data = malloc(0x60);
					if (e->data) {
						e->size = 0x60;
						memcpy(e->data, defBl60, 0x60);
					} else
						r = 1;
				}'''
FORMS = {}
for bk, bv in (('fail1st', BODY_F), ('ok1st', BODY_S)):
    FORMS['or_' + bk] = '\t\t\t\tif (loadBaseFile(e->name, e) || e->size != 0x60) ' + bv + '\n\t\t\t\tbreak;\n'
    FORMS['two_' + bk] = ('\t\t\t\tif (loadBaseFile(e->name, e)) ' + bv + ' else if (e->size != 0x60) ' + bv +
                          '\n\t\t\t\tbreak;\n')


def CASES(base):
    out = []
    for pk in ('plain', 'label'):
        for k, v in FORMS.items():
            def f(b, pk=pk, v=v):
                b = bdrun.sub(b, C24, v, 1)
                if pk == 'plain':
                    b = bdrun.sub(b, PRECHECK, '', 1)
                    b = bdrun.sub(b, TAIL, '\treturn 0;\n}', 1)
                return b
            out.append(('%s %s' % (pk, k), f))
    return out
