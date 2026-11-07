"""Attempt 28: block 116 is loadBl's flow scaled by the loadBl call site's frequency (6160 of the header's 9550: the none
test `strnicmp(..) || e->crc` at 29% + 71% x 50%).  116 < 88 needs the call site under about 5476, if the rest of the
layout survives the scaling.  The other loops in build.c spell the none test `if (!strnicmp(..) && !e->crc) continue;`
(PRED_CONTINUE on the skip), so try that and other loop-level spellings on the near miss (gen_bd390's PRE).
Behaviour: a skipped entry keeps r = 0, so the `if (r)` test is false either way.  Runs on src as of f2823155."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bd390 import PRE

OLD = '''		r = 0;
		if (strnicmp(e->name, "none", 4) || e->crc)
			loadBl(e, i, &r);
		if (r) {
'''
FORMS = {
    'src': OLD,
    'cont': '''		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		r = 0;
		loadBl(e, i, &r);
		if (r) {
''',
    'cont_r': '''		r = 0;
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		loadBl(e, i, &r);
		if (r) {
''',
    'nest': '''		r = 0;
		if (strnicmp(e->name, "none", 4) || e->crc) {
			loadBl(e, i, &r);
			if (r) {
''',
    'cont_eq': '''		if (strnicmp(e->name, "none", 4) == 0 && e->crc == 0)
			continue;
		r = 0;
		loadBl(e, i, &r);
		if (r) {
''',
}
NEST_END = '''			return -1;
		}
	}
	return 0;
}

int loadConsoleBlFiles(void)'''


def mk(b, f):
    b = bdrun.sub(b, OLD, FORMS[f], 1)
    if f == 'nest':
        b = bdrun.sub(b, NEST_END, NEST_END.replace('\t\t}\n\t}\n\treturn 0;', '\t\t\t}\n\t\t}\n\t}\n\treturn 0;', 1), 1)
        b = b.replace('''			if (r) {
			log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
			return -1;''', '''			if (r) {
				log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
				return -1;''', 1)
    return b


def CASES(base):
    return [(f, lambda b, f=f: mk(b, f)) for f in FORMS]


FOCUS = ['_loadBlFiles']
