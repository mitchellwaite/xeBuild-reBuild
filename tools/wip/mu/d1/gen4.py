"""gen4.py: helper whose error arm returns (39% early return + 29% call = 20.7%)."""
import gen3base as g
import sw

CALL2 = """			if (dumpDir)
				saveImage();
"""
SEP = 'log_printf(0, separator);'
E = g.ERR
vs = []
vs.append(('dup_sep', g.H("""	int r = writeImage(xb.outName);

	if (r) {
		%s
		%s
		return;
	}
	%s
""" % (E, SEP, SEP), CALL2)))
vs.append(('dup_sep_else', g.H("""	int r = writeImage(xb.outName);

	if (r) {
		%s
		%s
	} else
		%s
""" % (E, SEP, SEP), CALL2)))
vs.append(('dup_sep_int', g.H("""	int r = writeImage(xb.outName);

	if (r) {
		%s
		%s
		return r;
	}
	%s
	return 0;
""" % (E, SEP, SEP), CALL2, 'int')))
vs.append(('dup_sep_inline', g.BASE.replace(g.OLD, """			if (dumpDir) {
				r = writeImage(xb.outName);
				if (r) {
					%s
					%s
				} else
					%s
			}
""" % (E, SEP, SEP))))
print('param 68')
sw.run(vs, g.P68, save='gen4')
