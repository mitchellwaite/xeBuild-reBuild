"""Attempt 50: the CF/CG fallback as a shared helper (a50_share.py's su) in several bodies, in both
loaders or one, with nand (kv, kvAlt) or not; each with the hints off one at a time.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a50_su.py [-p 95,99]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import SU_FN, SU_OLD, SU_NEW, ANCHOR, split, sub, OFF

BASE = H.BASE
HEAD = '''/* a 5..21 bootloader from its file, or a CF/CG from the system update */
static uint32_t loadUpdateBl(struct fileent *e, int type)
{
'''
BODIES = {
    'var': SU_FN,
    # early returns
    'ret': HEAD + '''	uint32_t r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);

	if (!r)
		return 0;
	if (type == 9) {
		if (suGetCF(&e->data, &e->size))
			return 0;
	} else if (type == 10) {
		if (suGetCG(&e->data, &e->size))
			return 0;
	}
	return r;
}

''',
    # the loaded test first, then each type returns
    'ret2': HEAD + '''	uint32_t r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);

	if (r) {
		if (type == 9) {
			if (suGetCF(&e->data, &e->size))
				return 0;
		} else if (type == 10) {
			if (suGetCG(&e->data, &e->size))
				return 0;
		}
	}
	return r;
}

''',
    # the helper is only the fallback: called when the load failed
    'fb': '''/* a CF/CG that isn't in the input dir, from the system update */
static uint32_t updateBl(struct fileent *e, int type, uint32_t r)
{
	if (type == 9) {
		if (suGetCF(&e->data, &e->size))
			r = 0;
	} else if (type == 10) {
		if (suGetCG(&e->data, &e->size))
			r = 0;
	}
	return r;
}

''',
}
FB_NEW = '''				r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
				if (r)
					r = updateBl(e, type, r);
'''


def mk(body, where):
    def g(t):
        pre, lb, lc, post = split(t)
        new = FB_NEW if body == 'fb' else SU_NEW
        if 'B' in where:
            lb = sub(lb, SU_OLD, new)
        if 'C' in where:
            lc = sub(lc, SU_OLD, new)
        pre = sub(pre, ANCHOR, BODIES[body] + ANCHOR)
        return pre + lb + lc + post
    return g


V = {}
for body in BODIES:
    for where in ('BC', 'B', 'C'):
        for k in os.environ.get('A50_OFF', 'all,pr,lab,none').split(','):
            def f(t, body=body, where=where, p=OFF[k]):
                t = mk(body, where)(t)
                for a, b in p:
                    t = sub(t, a, b)
                return t
            V['%s_%s_%s' % (body, where, k)] = f
