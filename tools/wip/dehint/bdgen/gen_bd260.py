"""Attempt 15, exp_t24: the xell room test out of the xb.type chain, as addUpdateBls writes it (`if (type == 25 &&
e->offset < imgSize())` on its own after the chain).  Every type-25 entry the chain doesn't skip is a <=5 non-retail one,
so the behaviour is the same.  Axes: where the room test goes, the kit arm's form, the retail arm's form.
Runs on src/build.c as of 4c988f7c."""
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
KIT = '''				log_printf(1, "devkit/testkit image, skipping %s\\n", e->name);
				continue;
'''
WARN = '''			log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");
			continue;
'''

CHAIN = {
    # retail && (23||25) / else if kit { 23||25 }
    'c1': '''		if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {
''' + RET + '''		} else if (xb.type > BUILD_DEVGL16) {
			if (type == 23 || type == 25) {
''' + KIT + '''			}
		}
''',
    # two separate ifs
    'c2': '''		if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {
''' + RET + '''		}
		if (xb.type > BUILD_DEVGL16 && (type == 23 || type == 25)) {
''' + KIT + '''		}
''',
    # else if with &&
    'c3': '''		if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {
''' + RET + '''		} else if (xb.type > BUILD_DEVGL16 && (type == 23 || type == 25)) {
''' + KIT + '''		}
''',
    # the type test outside
    'c4': '''		if (type == 23 || type == 25) {
			if (xb.type == BUILD_RETAIL) {
''' + RET.replace('\t\t\t', '\t\t\t\t') + '''			} else if (xb.type > BUILD_DEVGL16) {
''' + KIT + '''			}
		}
''',
}

ROOM = {
    'and': '''		if (type == 25 && e->offset < imgSize()) {
''' + WARN + '''		}
''',
    'nest': '''		if (type == 25) {
			if (e->offset < imgSize()) {
''' + WARN.replace('\t\t\t', '\t\t\t\t') + '''			}
		}
''',
    'ge': '''		if (type == 25 && imgSize() > e->offset) {
''' + WARN + '''		}
''',
}


def mk(t, c, r, where):
    new = CHAIN[c] + ROOM[r]
    if where == 'after':
        return bdrun.sub(t, OLD, new, 1)
    raise ValueError(where)


def CASES(base):
    out = []
    for c, r in itertools.product(CHAIN, ROOM):
        out.append(('%s %s' % (c, r), lambda b, c=c, r=r: mk(b, c, r, 'after')))
    return out


FOCUS = ['_addBlsToImage']
