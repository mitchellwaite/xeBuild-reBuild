"""Attempt 30 helpers: src's seven loadBl hints off together (OFF7), and whole-function replacement of loadBl / loadBlFiles.

OFF7 removes exp_t10, exp_pr, lab_t5le, vol_fail, the `__builtin_constant_p` entry (both constant_p) and `else if (type)`;
pin_d (case 27) is kept unless a generator drops it.  setfn(text, head, new) swaps one whole function (head = its first line)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun, bdhints

CPBLK = '''		/* never taken, but the edge lasts until dom2 resolves
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
ELSETYPE = '''				/* Borderline, for review: type is 5, 11 or 17 here, so this test
				   is always true; a plain else costs 54 lines */
				} else if (type)
'''


def off7(b, keep=()):
    b = bdhints.off(b, *[h for h in ('exp_t10', 'exp_pr', 'lab_t5le', 'vol_fail') if h not in keep])
    if 'cp' not in keep:
        b = bdrun.sub(b, CPBLK, '', 1)
    if 'etype' not in keep:
        b = bdrun.sub(b, ELSETYPE, '				} else\n', 1)
    return b


def setfn(text, head, new):
    i, j = bdrun.fnspan(text, head)
    if not new.endswith('\n'):
        new += '\n'
    return text[:i] + new + text[j:]


LB = 'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)'
LBF = 'int loadBlFiles(void)'
