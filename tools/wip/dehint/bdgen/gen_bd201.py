"""Attempt 9, reconstruction B: src's loadBl helper (`*pr`) with every loadBl hint off, and subsets back on,
to compare with gen_bd200's loop on the same footing.  Runs on src/build.c as of f302f7d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints

CP_OLD = '''		/* never taken, but the edge lasts until dom2 resolves
		   __builtin_constant_p: an entry into vrp1's shared checkBl
		   copy whose type isn't a constant, so dom2's jump threads don't
		   scale the type == 11 test's frequency down to 0 (the original
		   places it by a frequency of ~25). The pointer compares set its
		   weight (tools/wip/README.md, build.c, eleventh pass) */
		if ((char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1) {
			type = (type & 1) + 18;
			goto chk;
		}
'''
DEAD_OLD = '''				/* Borderline, for review: type is 5, 11 or 17 here, so this test
				   is always true; a plain else costs 54 lines */
				} else if (type)'''
DEAD_NEW = '''				} else'''

HINTS = ['exp_t10', 'exp_pr', 'lab_t5le', 'lab_badsize', 'pin_d', 'vol_fail']


def make(base, on, cp, dead):
    t = bdhints.off(base, *[h for h in HINTS if h not in on])
    if not cp:
        t = t.replace(CP_OLD, '')
    if not dead:
        t = t.replace(DEAD_OLD, DEAD_NEW)
    return t


def CASES(base):
    out = [('none', lambda b: make(b, (), 0, 0))]
    for h in HINTS + ['cp', 'dead']:
        on = (h,) if h in HINTS else ()
        out.append(('+' + h, lambda b, on=on, h=h: make(b, on, h == 'cp', h == 'dead')))
    out.append(('+pin_d,vol_fail', lambda b: make(b, ('pin_d', 'vol_fail'), 0, 0)))
    out.append(('+pin_d,vol_fail,dead', lambda b: make(b, ('pin_d', 'vol_fail'), 0, 1)))
    out.append(('all but cp,dead', lambda b: make(b, HINTS, 0, 0)))
    return out


FOCUS = ['_loadBlFiles']
