"""gen18.py: drop the `ok` flag.  P(dumpDir) must lose its early-return share (78.3 -> 69.8) so the plain writeImage error reaches key 1: the dumpDir false edge must not go straight to the return block.
Shapes on the local-ret helper: duplicated tail with a return in the dump arm, ternary store, dump part as helper, etc.  Plus updateNand returning int."""
import axes as a
import cur2
import gen14
import gen16
import sw

E = cur2.ERR
IP = gen16.FORMS['c3']
WP = a.ERRS['plain']
TAIL = """			log_printf(0, "%s image built, info:\\n", xb.outName);
			*pret = ret;
"""


def base(w=WP, tail=TAIL):
    s = a.build(a.HEAD, a.REB['plain'], w, IP)
    assert TAIL in s
    return s.replace(TAIL, tail)


def c_local(s, drop_r=False):
    c0 = gen14.split(s, 'static void flashConsole(char *dumpDir, int *pret)', 'flashConsole(dumpDir, pret);')
    return c0.replace('{\n\tint r;\n\n\tnetUnmount', '{\n\t%sint ret = 0;\n\n\tnetUnmount' % ('' if drop_r else 'int r;\n\t'))


LOGB = 'log_printf(0, "%s image built, info:\\n", xb.outName);'
vs = []  # sweep body below runs on import too
vs.append(('dup_ret', c_local(base(w="""			if (dumpDir) {
				r = writeImage(xb.outName);
				if (r)
					%s
				log_printf(0, separator);
				%s
				*pret = ret;
				return;
			}
""" % (E, LOGB)))))
vs.append(('dup_else', c_local(base(w="""			if (dumpDir) {
				r = writeImage(xb.outName);
				if (r)
					%s
				log_printf(0, separator);
				%s
				*pret = ret;
			} else {
				%s
				*pret = ret;
			}
""" % (E, LOGB, LOGB), tail=''))))
vs.append(('dup_nolog', c_local(base(w="""			if (!dumpDir) {
				%s
				*pret = ret;
				return;
			}
			r = writeImage(xb.outName);
			if (r)
				%s
			log_printf(0, separator);
""" % (LOGB, E)))))
vs.append(('ternary', c_local(base(tail="""			log_printf(0, "%s image built, info:\\n", xb.outName);
			*pret = ret ? ret : 0;
"""))))
vs.append(('ifstore', c_local(base(tail="""			log_printf(0, "%s image built, info:\\n", xb.outName);
			if (ret)
				*pret = ret;
			else
				*pret = 0;
"""))))
vs.append(('store0', c_local(base(tail="""			log_printf(0, "%s image built, info:\\n", xb.outName);
			*pret = 0;
			if (ret)
				*pret = ret;
"""))))
sw.run(vs, '-O3', save='gen18')
