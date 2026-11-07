"""Attempt 30: the signature check's polarity without `else if (type)`.  With all of loadBl's hints off the verify test is
50/50 (PRED_CALL on both arms) and bb-reorder's tie picks the failed log as the fallthrough.  Forms that give the failed
edge its own predictor naturally:
  h_int   a static helper `int checkSig(e)` (no key: log, return 0; failed: log, return -1; passed: log, return 0),
          the caller `*pr = checkSig(e);` - if it isn't early inlined it has its own profile, where `return -1` gets
          PRED_NEGATIVE_RETURN on the failed edge only (frequencies are rebuilt from its probabilities at inlining)
  h_u32   the same returning uint32_t (CONST_RETURN for 0xffffffff)
  h_nest  h_int with src's nesting (`if (xb.pub1bl) { if (!verify) {..return -1;} passed } else nokey; return 0;`)
  h_ok    a BOOL helper (1 = ok or no key, 0 = failed), the caller `if (!checkSig(e)) *pr = -1;`
  s_tern  `*pr = cbVerifySig(..) ? 0 : -1;` then `if (*pr) failed log; else passed log;`
  s_set   `if (!cbVerifySig(..)) *pr = -1;` then `if (*pr) failed log; else passed log;`
  src     src's form (reference point)
on bases: ptr / retu, and9, c2, tail plain or src.  All seven loadBl hints off.  Runs on src as of 6083630d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
from a30lib import LB
import gen_bd411 as g

SRC_SIG = g.SIG['src']
FAILED = 'log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);'
PASSED = g.PASSED
NOKEY = g.NOKEY

HELPERS = {
    'h_int': '''/* check a 1BL-signed bootloader's signature: 0 if it passed or can't be checked */
static int checkSig(struct fileent *e)
{
	if (!xb.pub1bl) {
		%s
		return 0;
	}
	if (!cbVerifySig(e->data, xb.pub1bl)) {
		%s
		return -1;
	}
	%s
	return 0;
}

''' % (NOKEY, FAILED, PASSED),
    'h_nest': '''/* check a 1BL-signed bootloader's signature: 0 if it passed or can't be checked */
static int checkSig(struct fileent *e)
{
	if (xb.pub1bl) {
		if (!cbVerifySig(e->data, xb.pub1bl)) {
			%s
			return -1;
		}
		%s
	} else
		%s
	return 0;
}

''' % (FAILED, PASSED, NOKEY),
    'h_ok': '''/* check a 1BL-signed bootloader's signature: 0 if it failed */
static int checkSig(struct fileent *e)
{
	if (!xb.pub1bl) {
		%s
		return 1;
	}
	if (!cbVerifySig(e->data, xb.pub1bl)) {
		%s
		return 0;
	}
	%s
	return 1;
}

''' % (NOKEY, FAILED, PASSED),
}
HELPERS['h_u32'] = HELPERS['h_int'].replace('static int checkSig', 'static uint32_t checkSig')
HELPERS['h_nestu'] = HELPERS['h_nest'].replace('static int checkSig', 'static uint32_t checkSig')

CALL = {
    'h_int': '\t\t\t*pr = checkSig(e);\n',
    'h_u32': '\t\t\t*pr = checkSig(e);\n',
    'h_nest': '\t\t\t*pr = checkSig(e);\n',
    'h_nestu': '\t\t\t*pr = checkSig(e);\n',
    'h_ok': '\t\t\tif (!checkSig(e))\n\t\t\t\t*pr = -1;\n',
    's_tern': '''			if (xb.pub1bl) {
				*pr = cbVerifySig(e->data, xb.pub1bl) ? 0 : -1;
				if (*pr)
					%s
				else
					%s
			} else
				%s
''' % (FAILED, PASSED, NOKEY),
    's_set': '''			if (xb.pub1bl) {
				if (!cbVerifySig(e->data, xb.pub1bl))
					*pr = -1;
				if (*pr)
					%s
				else
					%s
			} else
				%s
''' % (FAILED, PASSED, NOKEY),
    'src': None,
}


def mk(b, res, sig, tail):
    t = g.mk(b, res, 'and9', 'c2', 'src', tail)
    i, j = bdrun.fnspan(t, 'static uint32_t loadBl(' if res == 'retu' else LB)
    f = t[i:j]
    if CALL[sig] is not None:
        call = CALL[sig] if res == 'ptr' else CALL[sig].replace('*pr', 'r')
        src_sig = SRC_SIG if res == 'ptr' else SRC_SIG.replace('*pr', 'r')
        f = bdrun.sub(f, src_sig, call, 1)
    t = t[:i] + HELPERS.get(sig, '') + f + t[j:]
    return t


PRE = g.PRE


def CASES(base):
    return [(' '.join(k), lambda b, k=k: mk(b, *k))
            for k in itertools.product(['ptr', 'retu'], list(CALL), ['plain', 'src'])]


FOCUS = ['_loadBlFiles']
