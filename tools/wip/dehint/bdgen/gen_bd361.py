"""Attempt 25, exp_t10: the update fallback clearing *pr on success (loadConsoleBlFiles' own shape, which landed exp_t9
in attempt 5) instead of breaking on failure, then one `if (*pr) break;`.  For a type-10 entry the SE test after it is
false, so the `goto chk` is optional.  Also gen_bd360's `and9` shape (28 loose without the expect, IDENTICAL with
it) in spellings without the empty statement.  Runs on src as of 3778d12d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''		if (*pr) {
			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (__builtin_expect(type == 10, 0)) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
		}
'''
CF = 'suGetCF(&e->data, &e->size)'
CG = 'suGetCG(&e->data, &e->size)'

ARMS = {
    # clear *pr when the update has the file
    'clr': '''		if (*pr) {
			if (type == 9) {
				if (%s)
					*pr = 0;
			} else if (type == 10) {
				if (%s)
					*pr = 0;
			}
		}
''' % (CF, CG),
    'clr_and': '''		if (*pr) {
			if (type == 9 && %s)
				*pr = 0;
			else if (type == 10 && %s)
				*pr = 0;
		}
''' % (CF, CG),
    'clr_flat': '''		if (*pr && type == 9 && %s)
			*pr = 0;
		else if (*pr && type == 10 && %s)
			*pr = 0;
''' % (CF, CG),
    'clr_10first': '''		if (*pr) {
			if (type == 10) {
				if (%s)
					*pr = 0;
			} else if (type == 9) {
				if (%s)
					*pr = 0;
			}
		}
''' % (CG, CF),
}
TAIL = {
    'brk': '''		if (*pr)
			break;
''',
    'brk_g10': '''		if (*pr)
			break;
		if (type == 10)
			goto chk;
''',
}
NOT = {
    'not9': '''		if (*pr) {
			if (!(type == 9 && %s)) {
				if (type == 10 && %s)
					goto chk;
				break;
			}
		}
''' % (CF, CG),
    'not9b': '''		if (*pr && !(type == 9 && %s)) {
			if (type == 10 && %s)
				goto chk;
			break;
		}
''' % (CF, CG),
    'or9': '''		if (*pr) {
			if (type == 10 && %s)
				goto chk;
			if (type != 9 || !%s)
				break;
		}
''' % (CG, CF),
    'nest9': '''		if (*pr) {
			if (type != 9 || !%s) {
				if (type != 10 || !%s)
					break;
				goto chk;
			}
		}
''' % (CF, CG),
}


def CASES(base):
    out = []
    for a, t in itertools.product(ARMS, TAIL):
        out.append(('%s %s' % (a, t), lambda b, a=a, t=t: bdrun.sub(b, OLD, ARMS[a] + TAIL[t], 1)))
    for n in NOT:
        out.append((n, lambda b, n=n: bdrun.sub(b, OLD, NOT[n], 1)))
    return out


FOCUS = ['_loadBlFiles']
