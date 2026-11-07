"""Attempt 27, exp_t10 on the and9 + c2 base (gen_bd380's c2base).  Diagnostic d1 (build/bd/a27/d1.c): the expect
moved from `type == 10` to the CG *success* test (`type == 10 && __builtin_expect(suGetCG(..) != 0, 0)`) is IDENTICAL,
so what the hint fixes is the CG success edge (61% from the failure break's early return), not the type == 10 edge.
Forms of the CG arm that give the success edge a predictor of its own: CG calling checkBl itself (attempt 16's
gen_bd272 idea, rerun on the new base: PRED_CALL on the success edge), CG success falling through to the SE test
(`nogo`), the success arm as a block with `goto chk`, and the failure as its own `break` (so the break isn't shared).
Each with exp_t10 kept or off.  Behaviour: for type 10 everything after chk: is a no-op (not 5/17/11, not 14), so
checkBl(.., 10, ..) then break is what goto chk did.  Runs on src as of 7a9a2b41."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun, bdhints
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bd380 as g380

OLD = '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (__builtin_expect(type == 10, 0) && suGetCG(&e->data, &e->size))
				goto chk;
			else
				break;
'''
T10 = {'exp': '__builtin_expect(type == 10, 0)', 'plain': 'type == 10'}
FORMS = {
    'base': OLD,
    'own10': '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (T10 && suGetCG(&e->data, &e->size)) {
				*pr = checkBl(e->data, e->size, 10, e->crc);
				break;
			} else
				break;
''',
    'owntype': '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (T10 && suGetCG(&e->data, &e->size)) {
				*pr = checkBl(e->data, e->size, type, e->crc);
				break;
			} else
				break;
''',
    'ownnest': '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (T10) {
				if (suGetCG(&e->data, &e->size))
					*pr = checkBl(e->data, e->size, 10, e->crc);
				break;
			} else
				break;
''',
    'nogo': '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (T10 && suGetCG(&e->data, &e->size))
				;
			else
				break;
''',
    'nest': '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (T10) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
''',
    'nest2': '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (T10) {
				if (suGetCG(&e->data, &e->size))
					goto chk;
				break;
			} else
				break;
''',
}


def mk(b, form, t10):
    b = g380.c2base(b)
    return bdrun.sub(b, OLD, FORMS[form].replace('T10', T10[t10]), 1)


def CASES(base):
    return [('%s %s' % (f, t), lambda b, a=(f, t): mk(b, *a)) for f, t in itertools.product(FORMS, T10)]


FOCUS = ['_loadBlFiles']
