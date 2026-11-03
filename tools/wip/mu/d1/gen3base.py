"""gen3base.py: BASE (mkcur.cur()), the writeImage block OLD, ERR and H(body, call, ret) to wrap it in a static helper saveImage."""
import mkcur
import gen1base as g1

P68 = g1.P68
BASE = mkcur.cur()
OLD = """			if (dumpDir) {
				r = writeImage(xb.outName);
				if (cp(r + 1) && cp(r + 2) && cp(r + 3) && cp(r + 4))
					goto werr;
				if (r)
				werr:
					log_printf(0, "\\n\\n***** ERROR: %i writing to file %s\\n\\n", r, xb.outName);
			wok: __attribute__((hot, unused));
				log_printf(0, separator);
			}
"""
assert OLD in BASE
ERR = 'log_printf(0, "\\n\\n***** ERROR: %i writing to file %s\\n\\n", r, xb.outName);'
HELPER_AT = 'static void updateNand(char *dumpDir, int *pret)\n'
assert HELPER_AT in BASE


def H(body, call, ret='void', base=None, old=None):
    """helper body + call replacing the block."""
    t = (base or BASE).replace(old or OLD, call)
    return t.replace(HELPER_AT, 'static %s saveImage(void)\n{\n%s}\n\n' % (ret, body) + HELPER_AT)
