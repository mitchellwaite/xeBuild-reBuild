"""Attempt 27: fallback orders and spellings with exp_t10 off, crossed with the constant_p weights of gen_bd382 (pp: src's,
pi: `pi it`, ip: `ii pt`), on the c2 base.  The weight re-tunes the type-11 block, so forms that attempt 25 scored on
src's weight (10 first: 100 loose, clear-on-success, ok flag) get a second look.  Behaviour as attempt 25's gen_bd360.
Runs on src as of 7a9a2b41."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bd380 as g380, gen_bd382 as g382

OLD = '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (__builtin_expect(type == 10, 0) && suGetCG(&e->data, &e->size))
				goto chk;
			else
				break;
'''
FORMS = {
    'and9': OLD.replace('__builtin_expect(type == 10, 0)', 'type == 10'),
    'g10first': '''			if (type == 10 && suGetCG(&e->data, &e->size))
				goto chk;
			if (type != 9 || !suGetCF(&e->data, &e->size))
				break;
''',
    'g10else': '''			if (type == 10 && suGetCG(&e->data, &e->size))
				goto chk;
			else if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else
				break;
''',
    'src': '''			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (type == 10) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
''',
    'src10': '''			if (type == 10) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else
				break;
''',
    'brk2': '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (type != 10 || !suGetCG(&e->data, &e->size))
				break;
			else
				goto chk;
''',
}
W = {'pp': ('pi', 'pt'), 'pi': ('pi', 'it'), 'ip': ('ii', 'pt')}


def mk(b, f, w):
    b = g380.c2base(b)
    b = bdrun.sub(b, OLD, FORMS[f], 1)
    return bdrun.sub(b, g382.CP_SRC, '%s && %s' % (g382.I[W[w][0]], g382.T[W[w][1]]), 1)


def CASES(base):
    return [('%s %s' % (f, w), lambda b, a=(f, w): mk(b, *a)) for f, w in itertools.product(FORMS, W)]


FOCUS = ['_loadBlFiles']
