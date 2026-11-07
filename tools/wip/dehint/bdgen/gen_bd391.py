"""Attempt 28: CG arm forms on the near miss (gen_bd390's PRE, src's if/else-if fallback), run with bddup.py to see the
dup and block 116's frequency.  CG calling checkBl itself (the Linux build has CG's own checkBl(10), attempt 9) puts
PRED_CALL on the CG success edge: DS(29%, 61%) = 39% (needs about 35%).  Behaviour: for type 10 everything after chk:
is a no-op (not 5/17/11, not 14, the t5le arm breaks with *pr = checkBl's result), so checkBl then break is goto chk.
Runs on src as of f2823155."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bd390 import PRE

OLD = '''			} else if (type == 10) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
'''
FORMS = {
    'src': OLD,
    'own10': '''			} else if (type == 10) {
				if (suGetCG(&e->data, &e->size))
					*pr = checkBl(e->data, e->size, 10, e->crc);
				break;
			} else
''',
    'owntype': '''			} else if (type == 10) {
				if (suGetCG(&e->data, &e->size))
					*pr = checkBl(e->data, e->size, type, e->crc);
				break;
			} else
''',
    'own10b': '''			} else if (type == 10) {
				if (!suGetCG(&e->data, &e->size))
					break;
				*pr = checkBl(e->data, e->size, 10, e->crc);
				break;
			} else
''',
    'nogo': '''			} else if (type == 10) {
				if (!suGetCG(&e->data, &e->size))
					break;
			} else
''',
    'go2': '''			} else if (type == 10) {
				if (suGetCG(&e->data, &e->size))
					goto chk;
				break;
			} else
''',
}


def CASES(base):
    return [(f, lambda b, f=f: bdrun.sub(b, OLD, FORMS[f], 1)) for f in FORMS]


FOCUS = ['_loadBlFiles']
