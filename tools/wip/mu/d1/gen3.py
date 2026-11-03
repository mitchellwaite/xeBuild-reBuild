"""gen3.py: writeImage error (needs key 1, was 2 plain): helper / early-return shapes replacing cp(r+N) and hot label wok."""
import mkcur
import sw
import gen1base as g

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


def H(body, call, ret='void'):
    """helper body + call replacing the block."""
    t = BASE.replace(OLD, call)
    return t.replace(HELPER_AT, 'static %s saveImage(void)\n{\n%s}\n\n' % (ret, body) + HELPER_AT)


CALL = """			if (dumpDir) {
				saveImage();
				log_printf(0, separator);
			}
"""
vs = []
vs.append(('plain', BASE.replace(OLD, """			if (dumpDir) {
				r = writeImage(xb.outName);
				if (r)
					%s
				log_printf(0, separator);
			}
""" % ERR)))
vs.append(('h_ret_early', H("""	int r = writeImage(xb.outName);

	if (!r)
		return;
	%s
""" % ERR, CALL)))
vs.append(('h_plain', H("""	int r = writeImage(xb.outName);

	if (r)
		%s
""" % ERR, CALL)))
vs.append(('h_int_early', H("""	int r = writeImage(xb.outName);

	if (!r)
		return 0;
	%s
	return r;
""" % ERR, CALL, 'int')))
vs.append(('h_int_ret1', H("""	int r = writeImage(xb.outName);

	if (r) {
		%s
		return 1;
	}
	return 0;
""" % ERR, CALL, 'int')))
vs.append(('h_int_ret_neg', H("""	int r = writeImage(xb.outName);

	if (r) {
		%s
		return -1;
	}
	return 0;
""" % ERR, CALL, 'int')))
vs.append(('h_sep_inside', H("""	int r = writeImage(xb.outName);

	if (!r) {
		log_printf(0, separator);
		return;
	}
	%s
	log_printf(0, separator);
""" % ERR, """			if (dumpDir)
				saveImage();
""")))
vs.append(('h_sep_inside2', H("""	int r = writeImage(xb.outName);

	if (r)
		%s
	log_printf(0, separator);
""" % ERR, """			if (dumpDir)
				saveImage();
""")))
vs.append(('inl_goto', BASE.replace(OLD, """			if (dumpDir) {
				r = writeImage(xb.outName);
				if (!r)
					goto wok;
				%s
			wok:
				log_printf(0, separator);
			}
""" % ERR)))
vs.append(('inl_nz', BASE.replace(OLD, """			if (dumpDir) {
				if ((r = writeImage(xb.outName)) != 0)
					%s
				log_printf(0, separator);
			}
""" % ERR)))
print('param 68')
sw.run(vs, g.P68, save='gen3')
