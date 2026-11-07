"""Attempt 25, exp_t10: loadBl's update fallback (CF from suGetCF, CG from suGetCG) in other natural orders and
nestings, expect off (and on, for reference).  Attempt 1's gen_bd18 swept the 9/10 order with most of today's other
hints different; attempt 21 measured the CG flow as 50% x 86.3% x 19.9% x 61% (needs about half).  Every form keeps
the behaviour: a type-10 entry that suGetCG fills reaches chk with type 10 (the SE test is false for it), a type-9
entry that suGetCF fills goes through the SE test, any other failure breaks with *pr as loadInputFile left it.
Runs on src as of 3778d12d."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun, bdhints

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
F = {
    'src': OLD.replace('__builtin_expect(type == 10, 0)', 'type == 10'),
    'src_exp': OLD,
    # 10 first
    'g10first': '''		if (*pr) {
			if (type == 10) {
				if (!%s)
					break;
				goto chk;
			} else if (type == 9) {
				if (!%s)
					break;
			} else
				break;
		}
''' % (CG, CF),
    # positive call tests
    'pos': '''		if (*pr) {
			if (type == 9) {
				if (%s)
					goto se;
			} else if (type == 10) {
				if (%s)
					goto chk;
			}
			break;
		}
	se:
''' % (CF, CG),
    # the non-update types break first
    'nonupd': '''		if (*pr) {
			if (type != 9 && type != 10)
				break;
			if (type == 9) {
				if (!%s)
					break;
			} else {
				if (!%s)
					break;
				goto chk;
			}
		}
''' % (CF, CG),
    'else10': '''		if (*pr) {
			if (type == 9) {
				if (!%s)
					break;
			} else {
				if (type != 10 || !%s)
					break;
				goto chk;
			}
		}
''' % (CF, CG),
    'and9': '''		if (*pr) {
			if (type == 9 && %s)
				;
			else if (type == 10 && %s)
				goto chk;
			else
				break;
		}
''' % (CF, CG),
    'neg10': '''		if (*pr) {
			if (type == 9) {
				if (!%s)
					break;
			} else if (type != 10)
				break;
			else {
				if (!%s)
					break;
				goto chk;
			}
		}
''' % (CF, CG),
    'cg_ret': '''		if (*pr) {
			if (type == 10) {
				if (%s)
					goto chk;
				break;
			}
			if (type != 9 || !%s)
				break;
		}
''' % (CG, CF),
    'ok_flag': '''		if (*pr) {
			int ok = 0;

			if (type == 9)
				ok = %s;
			else if (type == 10)
				ok = %s;
			if (!ok)
				break;
			if (type == 10)
				goto chk;
		}
''' % (CF, CG),
    'lone10': '''		if (*pr) {
			if (type == 10) {
				if (!%s)
					break;
				goto chk;
			}
			if (type == 9) {
				if (!%s)
					break;
			} else
				break;
		}
''' % (CG, CF),
}


def mk(t, k):
    t = bdrun.sub(t, OLD, F[k], 1)
    if k == 'pos':
        # the label sits before the SE test
        t = bdrun.sub(t, '''	se:
		if (type == 9 && e->data[0]''', '''	se:
		if (type == 9 && e->data[0]''', 1)
    return t


def CASES(base):
    return [(k, lambda b, k=k: mk(b, k)) for k in F]


FOCUS = ['_loadBlFiles']
