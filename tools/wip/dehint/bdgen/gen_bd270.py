"""Attempt 16, exp_t24: the kit arm as `else if (xb.type > BUILD_DEVGL16 && (type == 23 || type == 25))`, the same
shape as the retail arm above it, with the room test still in the else-if chain.  Same behaviour: a kit entry of
another type now reaches `type == 25 && ..`, which is false for it.  The idea: that flow enters the type == 25 test at
profile_estimate (raising the warning's estimate) and is threaded out later by vrp1/dom.  Axes: kit arm form, room
test form, retail arm form.  Runs on src/build.c as of e76f027f."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''		if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {
			log_printf(1, "retail image, skipping %s\\n", e->name);
			continue;
		} else if (xb.type > BUILD_DEVGL16) {
			if (type == 23 || type == 25) {
				log_printf(1, "devkit/testkit image, skipping %s\\n", e->name);
				continue;
			}
		} else if (type == 25 && __builtin_expect(type != 24, 1) && e->offset < imgSize()) {
			log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");
			continue;
		}
'''
RET = '''			log_printf(1, "retail image, skipping %s\\n", e->name);
			continue;
'''
KIT = '''			log_printf(1, "devkit/testkit image, skipping %s\\n", e->name);
			continue;
'''
WARN = '''			log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");
			continue;
'''
KITC = {
    'and': 'xb.type > BUILD_DEVGL16 && (type == 23 || type == 25)',
    'andr': '(type == 23 || type == 25) && xb.type > BUILD_DEVGL16',
    'ge6': 'xb.type >= BUILD_DEVKIT && (type == 23 || type == 25)',
}
RETC = {
    'r': 'xb.type == BUILD_RETAIL && (type == 23 || type == 25)',
    'rr': '(type == 23 || type == 25) && xb.type == BUILD_RETAIL',
}
ROOMC = {
    'p': 'type == 25 && e->offset < imgSize()',
    'g': 'type == 25 && imgSize() > e->offset',
    'k': 'type == 25 && xb.type <= BUILD_DEVGL16 && e->offset < imgSize()',
}


def mk(t, k, r, m):
    new = ('\t\tif (%s) {\n' % RETC[r] + RET + '\t\t} else if (%s) {\n' % KITC[k] + KIT +
           '\t\t} else if (%s) {\n' % ROOMC[m] + WARN + '\t\t}\n')
    return bdrun.sub(t, OLD, new, 1)


def CASES(base):
    out = []
    for k, r, m in itertools.product(KITC, RETC, ROOMC):
        out.append(('%s %s %s' % (k, r, m), lambda b, k=k, r=r, m=m: mk(b, k, r, m)))
    return out


FOCUS = ['_addBlsToImage']
