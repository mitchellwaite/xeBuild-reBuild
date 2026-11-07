"""Attempt 31: the size log's -1 on attempt 30's c6 near miss (case 6 first + and9 + fail closing case 2, barrier off:
1 loose / 7 strict).  Case 23's forms: own -1 after / before the log, `return`, nested under `if (!*pr)`, the test as
`e->size & 3`, good path first, the retail test wrapping the arm, the size test before the load-result test (only
as a diagnostic: it reads e->size of a failed load), and case 2's smc test in other spellings (`if (!e->offset)
{ fail: .. }`).  Runs on src as of 48ce6ada."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
import gen_bd420 as g20

LOG = 'log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);'
C23 = '''		*pr = loadBinFile(e);
		if (*pr)
			break;
		/* Borderline, for review: loadConsoleBlFiles spells this test
		   e->size & 3.  Here a compare of two non-constants gets the
		   nonequal heuristic on top of the early return, so the
		   appendAddonPatches arm is cold enough for bb-reorder's last
		   round (it replaces a hot label) */
		if ((e->size & ~3) != e->size) {
			LOG
			goto fail;
		}
		appendAddonPatches(e);
		break;
'''.replace('LOG', LOG)
TEST = '(e->size & ~3) != e->size'
GOOD = '(e->size & ~3) == e->size'

FORMS = {
    'src': None,
    'own': '''		*pr = loadBinFile(e);
		if (*pr)
			break;
		if (T) {
			LOG
			*pr = -1;
			break;
		}
		appendAddonPatches(e);
		break;
''',
    'ownpre': '''		*pr = loadBinFile(e);
		if (*pr)
			break;
		if (T) {
			*pr = -1;
			LOG
			break;
		}
		appendAddonPatches(e);
		break;
''',
    'ownret': '''		*pr = loadBinFile(e);
		if (*pr)
			break;
		if (T) {
			LOG
			*pr = -1;
			return;
		}
		appendAddonPatches(e);
		break;
''',
    'nest': '''		*pr = loadBinFile(e);
		if (!*pr) {
			if (T) {
				LOG
				goto fail;
			}
			appendAddonPatches(e);
		}
		break;
''',
    'nestelse': '''		*pr = loadBinFile(e);
		if (!*pr) {
			if (G)
				appendAddonPatches(e);
			else {
				LOG
				goto fail;
			}
		}
		break;
''',
    'nestown': '''		*pr = loadBinFile(e);
		if (!*pr) {
			if (T) {
				LOG
				*pr = -1;
			} else
				appendAddonPatches(e);
		}
		break;
''',
    'good': '''		*pr = loadBinFile(e);
		if (*pr)
			break;
		if (G) {
			appendAddonPatches(e);
			break;
		}
		LOG
		goto fail;
''',
    'diag_szfirst': '''		*pr = loadBinFile(e);
		if (T) {
			LOG
			goto fail;
		}
		if (*pr)
			break;
		appendAddonPatches(e);
		break;
''',
}
TESTS = {'ne': (TEST, GOOD), 'and3': ('e->size & 3', '!(e->size & 3)')}

RETAIL = '''		if (xb.type == BUILD_RETAIL)
			break;
		*pr = loadBinFile(e);'''

C2 = '''		if (e->offset)
			break;
	fail:
			*pr = -1;
		break;
'''
C2V = {
    'c2': None,
    'c2blk': '''		if (!e->offset) {
	fail:
			*pr = -1;
		}
		break;
''',
}


def mk(b, form, test, c2):
    b = g20.mk(b, 'and9', 'c2', 0)
    if form != 'src' or test != 'ne':
        f = FORMS[form] if form != 'src' else C23.replace('\t\t/* Borderline', '\t\t/*X').split('\t\t/*X')[0] + '''		if (T) {
			LOG
			goto fail;
		}
		appendAddonPatches(e);
		break;
'''
        t, g = TESTS[test]
        b = bdrun.sub(b, C23, f.replace('LOG', LOG).replace('(T)', '(' + t + ')').replace('(G)', '(' + g + ')'), 1)
    if C2V[c2]:
        b = bdrun.sub(b, C2, C2V[c2], 1)
    return b


def CASES(base):
    return [(' '.join(k), lambda b, k=k: mk(b, *k)) for k in itertools.product(list(FORMS), list(TESTS), list(C2V))]


FOCUS = ['_loadBlFiles']
