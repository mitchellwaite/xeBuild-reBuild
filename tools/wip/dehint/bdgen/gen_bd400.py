"""Attempt 29: take the CG failure's and the other types' early returns away by joining the arm's failures at the
checkBl result test (`if (*pr) break;` after chk) instead of breaking to loadBl's return block.  At profile_estimate
the failure edges then go to a test, not the return block, so PRED_TREE_EARLY_RETURN doesn't fire on them: p10 13.7%,
s10 50%, CGok 15.2, block 116 about 86 by attempt 28's formula.  vrp1 threads each failure path (r != 0 known) through
the result test to the break.  Run with bddup.py on the near miss (gen_bd390's PRE).  Runs on src as of 1caeb924."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bd390 import PRE

LOAD = '''		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (*pr) {
			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (type == 10) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
		}
		if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {
			/* an SE where the CF goes */
			e->type = type = 14;
			xb.cfLdv = 0;
			xb.seReplacesCf = 1;
		}
	chk:
		*pr = checkBl(e->data, e->size, type, e->crc);
		if (*pr)
			break;
'''
SEB = '''		if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {
			/* an SE where the CF goes */
			e->type = type = 14;
			xb.cfLdv = 0;
			xb.seReplacesCf = 1;
		}
'''
SEI = SEB.replace('\n\t\t', '\n\t\t\t').replace('\t\tif (type == 9 &&', '\t\t\tif (type == 9 &&', 1)


def fb(cf, cg, other):
    return '''		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (*pr) {
			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					%s;
			} else if (type == 10) {
				if (!suGetCG(&e->data, &e->size))
					%s;
				goto chk;
			} else
				%s;
		}
''' % (cf, cg, other)


TAILRES = '''	chk:
		*pr = checkBl(e->data, e->size, type, e->crc);
	res:
		if (*pr)
			break;
'''
FORMS = {
    'src': LOAD,
    'res_all': fb('goto res', 'goto res', 'goto res') + SEB + TAILRES,
    'res_cg_else': fb('break', 'goto res', 'goto res') + SEB + TAILRES,
    'res_cg': fb('break', 'goto res', 'break') + SEB + TAILRES,
    'res_else': fb('break', 'break', 'goto res') + SEB + TAILRES,
    # checkBl only when the image is there: the failures skip the block and meet its result test
    'blk_g': '''		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (*pr) {
			if (type == 9) {
				if (suGetCF(&e->data, &e->size))
					goto se;
			} else if (type == 10) {
				if (suGetCG(&e->data, &e->size))
					goto chk;
			}
		} else {
		se:
''' + SEI + '''		chk:
			*pr = checkBl(e->data, e->size, type, e->crc);
		}
		if (*pr)
			break;
''',
    # the CF / CG success as an `ok` condition of the checkBl block
    'cond': '''		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (!*pr || (type == 9 && suGetCF(&e->data, &e->size))) {
''' + SEI + '''		chk:
			*pr = checkBl(e->data, e->size, type, e->crc);
		} else if (type == 10 && suGetCG(&e->data, &e->size))
			goto chk;
		if (*pr)
			break;
''',
}


def CASES(base):
    return [(f, lambda b, f=f: bdrun.sub(b, LOAD, FORMS[f], 1)) for f in FORMS]


FOCUS = ['_loadBlFiles']
