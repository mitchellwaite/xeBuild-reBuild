"""Attempt 21, loadBl's tail (t5le, exp_pr, the barrier): attempt 20's lever, the deciding test repeated where each
path uses it, so the signature-failed (*pr = -1) and the *pr = 0 paths reach separate `xb.type <= 5` tests before
profile_estimate instead of vrp1's joiner copies of one.  Axes: tail form x hints kept (t5le / exp_pr, where the form
still has the `*pr` test) x size-log form (src's goto fail with the barrier, or attempt 10's own `*pr = -1; break;`
with the barrier off).  Runs on src as of c7114455."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

TAIL = '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
	case 6:
'''
SET = '''		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
	case 6:
'''
K = 'xb.type <= BUILD_DEVGL16'
G = 'xb.type > BUILD_DEVGL16'
FORMS = {
    'src': '''		if (@K@) {
			if (@PR@)
				goto fail;
			break;
		}
''' + SET,
    # *pr tested first, the <=5 test in each arm
    'prfirst': '''		if (@PR@) {
			if (@K@)
				goto fail;
		} else if (@K@)
			break;
''' + SET,
    'prfirst2': '''		if (@PR@) {
			if (@K@)
				goto fail;
		} else {
			if (@K@)
				break;
		}
''' + SET,
    # the failure exit and the <=5 exit as two tests of xb.type
    'and_pr_k': '''		if (@PR@ && @K@)
			goto fail;
		if (@K@)
			break;
''' + SET,
    'and_k_pr': '''		if (@K@ && @PR@)
			goto fail;
		if (@K@)
			break;
''' + SET,
    'and_k_pr_g': '''		if (@K@ && @PR@)
			goto fail;
		if (@G@ && type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
	case 6:
''',
    'and_pr_k_g': '''		if (@PR@ && @K@)
			goto fail;
		if (@G@ && type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
	case 6:
''',
    # <=5 tested twice: once for the failure, once to skip setFlashBuild
    'kk': '''		if (@K@) {
			if (@PR@)
				goto fail;
		}
		if (@K@)
			break;
''' + SET,
    'kk_g': '''		if (@K@) {
			if (@PR@)
				goto fail;
		}
		if (@G@ && type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
	case 6:
''',
    'k_else': '''		if (@K@) {
			if (@PR@)
				goto fail;
		} else if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
	case 6:
''',
    # *pr first, then the whole tail per arm
    'pr_split': '''		if (@PR@) {
			if (@K@)
				goto fail;
			if (type == 14)
				setFlashBuild(getBeU16(xb.files[i].data + 2));
			break;
		}
		if (@K@)
			break;
''' + SET,
}
PRS = {'ne': '*pr != 0', 'b': '*pr', 'm1': '*pr == -1'}
SIZE_OLD = '''			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			goto fail;
'''
SIZE_NEW = '''			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			*pr = -1;
			break;
'''


def mk(b, form, pr, ep, size):
    t = b
    p = PRS[pr]
    if ep:
        p = '__builtin_expect(%s, 0)' % p
    f = FORMS[form].replace('@PR@', p).replace('@K@', K).replace('@G@', G)
    t = bdrun.sub(t, TAIL, f)
    if size == 'brk':
        t = bdrun.sub(t, SIZE_OLD, SIZE_NEW)
        t = bdhints.off(t, 'vol_fail')
    return t


def CASES(base):
    out = []
    for form, pr, ep, size in itertools.product(FORMS, PRS, [0, 1], ['src', 'brk']):
        out.append(('%s %s %s %s' % (form, pr, 'exp' if ep else '-', size), lambda b, c=(form, pr, ep, size): mk(b, *c)))
    return out


FOCUS = ['_loadBlFiles']
