"""Attempt 30: the c6 near miss (case 6 first + and9 + fail closing case 2, barrier off: 1 loose / 7 strict, only the size
log's own -1).  Axes around it: tail (src with t5le + exp_pr / without t5le / without exp_pr / both off / attempt 10's
plain), size arm (src; `else` order: good path first and the log then `goto fail`; the -1 written before the log as
`{ *pr = -1; log; break; }` is not behaviour-neutral for .. it is: the log reads e->size only), sig-failed order (`*pr = -1`
before the log), result (ptr / retu).  Runs on src as of 6083630d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun, bdhints
import a30lib
import gen_bd420 as g20

TAILS = {'src': (), 'nt5': ('lab_t5le',), 'npr': ('exp_pr',), 'both': ('lab_t5le', 'exp_pr'), 'plain': 'plain'}
SRC_TAIL = '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		}
'''
PLAIN = '''		if (xb.type <= BUILD_DEVGL16)
			break;
'''
SZ = g20.SZ
SZ_ELSE = '''		if ((e->size & ~3) == e->size) {
			appendAddonPatches(e);
			break;
		}
		log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
		goto fail;
'''
SZ_IF = '''		if ((e->size & ~3) != e->size) {
			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			goto fail;
		} else
			appendAddonPatches(e);
		break;
'''
SIGF = '''					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					*pr = -1;
'''
SIGF2 = '''					*pr = -1;
					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
'''


def mk(b, tail, sz, sigf):
    b = g20.mk(b, 'and9', 'c2', 0)
    if tail == 'plain':
        b = bdrun.sub(b, SRC_TAIL, PLAIN, 1)
    else:
        b = bdhints.off(b, *TAILS[tail]) if TAILS[tail] else b
    if sz == 'else':
        b = bdrun.sub(b, SZ, SZ_ELSE, 1)
    elif sz == 'if':
        b = bdrun.sub(b, SZ, SZ_IF, 1)
    if sigf:
        b = bdrun.sub(b, SIGF, SIGF2, 1)
    return b


def CASES(base):
    return [(' '.join(map(str, k)), lambda b, k=k: mk(b, *k)) for k in itertools.product(list(TAILS), ['src', 'else', 'if'], [0, 1])]


FOCUS = ['_loadBlFiles']
