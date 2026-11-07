"""Attempt 21, diagnostics (not shapes): gen_bd320's `prfirst` tail (the `*pr` test first, the `<=5` test in each arm, so
each path has its own test at profile_estimate) with expects on each arm's `<=5` test, to find what each test's
probability must be.  t5le gone in every case; the outer `*pr` test with or without its expect."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

TAIL = '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		}
'''
K = 'xb.type <= BUILD_DEVGL16'
FORM = '''		if (@PR@) {
			if (@K1@)
				@X1@;
		} else if (@K0@)
			break;
'''


def wrap(k, e):
    return k if e is None else '__builtin_expect(%s, %d)' % (k, e)


def mk(b, ep, e1, e0, x1):
    f = FORM.replace('@PR@', wrap('*pr != 0', 0 if ep else None)).replace('@K1@', wrap(K, e1)).replace('@K0@', wrap(K, e0))
    f = f.replace('@X1@', 'goto fail' if x1 == 'fail' else 'break')
    return bdrun.sub(b, TAIL, f)


def CASES(base):
    out = []
    for c in itertools.product([0, 1], [None, 0, 1], [None, 0, 1], ['fail', 'brk']):
        out.append(('ep%d e1=%s e0=%s %s' % c, lambda b, c=c: mk(b, *c)))
    return out


FOCUS = ['_loadBlFiles']
