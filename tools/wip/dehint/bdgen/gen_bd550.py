"""Attempt 43: on attempt 42's wt / no-param near miss (gen_bd540's wt base with exp_t10, exp_pr and lab_t5le off), tail
forms for the SE copy's `ja` and the T test's q, and two loop-level forms for the dup's threshold.  Run without the
param: `BDEXTRA='--param builtin-expect-probability=90' python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd550.py -n 100`
(90 is gcc's default, so this is the no-`--param` build; bdrun always passes 98 first and the later --param wins)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
from gen_bd540 import BASES, offs

FOCUS = ['_loadBlFiles']


def PRE(t):
    return offs(BASES['wt'](t), ('exp_t10', 'exp_pr', 'lab_t5le'))


TAIL = '''		if (xb.type <= BUILD_DEVGL16) {
			if (*pr != 0)
				goto fail;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
'''
TAILS = {
    'base': TAIL,
    'eqm1': TAIL.replace('*pr != 0', '*pr == (uint32_t)-1'),
    'neg': TAIL.replace('*pr != 0', '(int)*pr < 0'),
    'elif': '''		if (xb.type <= BUILD_DEVGL16) {
			if (*pr)
				goto fail;
		} else if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''',
    'kitelse': '''		if (xb.type > BUILD_DEVGL16) {
			if (type == 14)
				setFlashBuild(getBeU16(xb.files[i].data + 2));
		} else if (*pr)
			goto fail;
		break;
''',
    'kitfirst': '''		if (xb.type > BUILD_DEVGL16) {
			if (type == 14)
				setFlashBuild(getBeU16(xb.files[i].data + 2));
			break;
		}
		if (*pr)
			goto fail;
		break;
''',
    'and': '''		if (xb.type <= BUILD_DEVGL16 && *pr)
			goto fail;
		if (xb.type > BUILD_DEVGL16 && type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''',
    'and14': '''		if (type == 14 && xb.type > BUILD_DEVGL16)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		else if (xb.type <= BUILD_DEVGL16 && *pr)
			goto fail;
		break;
''',
    'retfail': '''		if (xb.type <= BUILD_DEVGL16) {
			if (!*pr)
				break;
			goto fail;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''',
    'nest14': '''		if (xb.type <= BUILD_DEVGL16) {
			if (*pr)
				goto fail;
		} else {
			if (type == 14)
				setFlashBuild(getBeU16(xb.files[i].data + 2));
		}
		break;
''',
}


def CASES(base):
    out = []
    for k, v in TAILS.items():
        out.append((k, lambda t, v=v: bdrun.sub(t, TAIL, v, 1)))
    return out
