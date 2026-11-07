"""Attempt 24, exp_t24: the kit arm in the else-if chain (`else if (xb.type > BUILD_DEVGL16 && (..))`, the retail
arm's shape, attempt 16's gen_bd270) with the two type tests in either order, and the retail arm's order too.  The
kit-in-chain form gives the kit path's not-23/25 flow to the `type == 25` test at profile_estimate (the warning's
frequency rises), and vrp1 threads that flow past the test only when its first assert on the kit-false edge is
`type != 25` (lhs_of_dominating_assert takes the first ASSERT_EXPR of `type`; the second is chained on the first).
Runs on src as of 892a28f1."""
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
    'k23': 'xb.type > BUILD_DEVGL16 && (type == 23 || type == 25)',
    'k25': 'xb.type > BUILD_DEVGL16 && (type == 25 || type == 23)',
    'k25ge': 'xb.type >= BUILD_DEVKIT && (type == 25 || type == 23)',
    'k25np': 'xb.type > BUILD_DEVGL16 && (type == 25 || type == 23)',  # same, kept for the nested-room axis
}
RETC = {
    'r23': 'xb.type == BUILD_RETAIL && (type == 23 || type == 25)',
    'r25': 'xb.type == BUILD_RETAIL && (type == 25 || type == 23)',
}
ROOM = {
    'flat': lambda: '\t\t} else if (type == 25 && e->offset < imgSize()) {\n' + WARN + '\t\t}\n',
    'nest': lambda: ('\t\t} else if (type == 25) {\n\t\t\tif (e->offset < imgSize()) {\n' +
                     WARN.replace('\t\t\t', '\t\t\t\t') + '\t\t\t}\n\t\t}\n'),
}


def mk(t, k, r, m):
    new = ('\t\tif (%s) {\n' % RETC[r] + RET + '\t\t} else if (%s) {\n' % KITC[k] + KIT + ROOM[m]())
    return bdrun.sub(t, OLD, new, 1)


def CASES(base):
    out = []
    for k, r, m in itertools.product(KITC, RETC, ROOM):
        if k == 'k25np':
            continue
        out.append(('%s %s %s' % (k, r, m), lambda b, k=k, r=r, m=m: mk(b, k, r, m)))
    return out


FOCUS = ['_addBlsToImage']
