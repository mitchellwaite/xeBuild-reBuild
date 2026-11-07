"""Attempt 20, loadFileCrc (exp_verbose + pin_e): the "reading" logs as a helper, both hints off.  A helper with two calls
isn't early inlined, so at profile_estimate loadFileCrc's verbose arm is one call (PRED_CALL), and the helper's own
profile (nonequal on size != len) is scaled in at IPA; the non-pad path's thread into the bytes log then happens in the
inlined copy.  Forms: verbose tested outside or inside, early return or if/else, the padded size passed as e->size or
recomputed, e passed in, the helper before loadFileCrc.  Runs on src as of a0108d6d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

OLD = '''	/* hints: the "bytes" log must be hot enough for bb-reorder's second round
	   (build.sh's expect probability, 92-99); the pin sets e's register in the
	   out-of-line copy only (callers with pad == 0 drop this block) */
	if (verbose) {
		if (size != e->size) {
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, align16(size));
		} else
			log_printf(1, "reading %s (0x%x bytes)", name, size);
	}
'''
ANCHOR = 'int loadFileCrc(const char *name, struct fileent *e, int verbose, int pad, uint32_t crc)\n{'

P_LEN = 'log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, len);'
P_AL = 'log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, align16(size));'
B = 'log_printf(1, "reading %s (0x%x bytes)", name, size);'

BODIES = {
    'ifelse': '\tif (size != len)\n\t\t%(P)s\n\telse\n\t\t%(B)s\n',
    'ifelse_eq': '\tif (size == len)\n\t\t%(B)s\n\telse\n\t\t%(P)s\n',
    'ret': '\tif (size == len) {\n\t\t%(B)s\n\t\treturn;\n\t}\n\t%(P)s\n',
    'ret_ne': '\tif (size != len) {\n\t\t%(P)s\n\t\treturn;\n\t}\n\t%(B)s\n',
}


def mk(b, body, vin, plen, sig, call_len):
    P = P_LEN if plen else P_AL
    bb = BODIES[body] % {'P': P, 'B': B}
    if vin:
        bb = '\tif (!verbose)\n\t\treturn;\n' + bb
    if sig == 'len':
        params = 'const char *name, uint32_t size, uint32_t len'
        arg = 'name, size, e->size' if call_len == 'e' else 'name, size, align16(size)'
        pre = ''
    else:  # e passed: len read inside
        params = 'const char *name, struct fileent *e, uint32_t size'
        arg = 'name, e, size'
        pre = '\tuint32_t len = e->size;\n\n'
        if call_len != 'e':
            return None
    if vin:
        params += ', int verbose'
        arg += ', verbose'
    helper = 'static void logReading(%s)\n{\n%s%s}\n\n' % (params, pre, bb)
    call = ('\tlogReading(%s);\n' % arg) if vin else ('\tif (verbose)\n\t\tlogReading(%s);\n' % arg)
    t = bdhints.off(b, 'pin_e', 'exp_verbose')
    old = OLD.replace('if (__builtin_expect(verbose, 1)) {', 'if (verbose) {').replace('\t\t\t__asm__("" : : "S"(e));\n', '')
    t = bdrun.sub(t, old, call)
    t = bdrun.sub(t, ANCHOR, helper + ANCHOR)
    return t


def CASES(base):
    out = []
    for c in itertools.product(BODIES, [0, 1], [0, 1], ['len', 'e'], ['e', 'al']):
        out.append(('%s vin%d plen%d %s %s' % c, lambda b, c=c: mk(b, *c)))
    return out


FOCUS = ['_loadFileCrc']
