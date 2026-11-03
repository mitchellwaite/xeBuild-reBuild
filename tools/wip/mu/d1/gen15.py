"""gen15.py: with the flashConsole helper, try to get the natural -ip arm (form b/a/d) and the plainest writeImage test.
Axes: helper signature (changes SSA numbering, which decides the -ip test order), `ok` spelling and scope, helper's locals, -ip form."""
import itertools

import axes as a
import cur2
import gen14
import sw

E = cur2.ERR
SIG = {
    's0': ('static void flashConsole(char *dumpDir, int ret, int *pret)', 'flashConsole(dumpDir, ret, pret);'),
    's1': ('static void flashConsole(int ret, char *dumpDir, int *pret)', 'flashConsole(ret, dumpDir, pret);'),
    's2': ('static void flashConsole(char *dumpDir, int *pret, int ret)', 'flashConsole(dumpDir, pret, ret);'),
    's3': ('static void flashConsole(int *pret, char *dumpDir, int ret)', 'flashConsole(pret, dumpDir, ret);'),
}


def err(pre, c):
    return """			if (dumpDir) {
				r = writeImage(xb.outName);
				%s
				if (%s)
					%s
				log_printf(0, separator);
			}
""" % (pre, c, E)


def err2(s):
    return """			if (dumpDir) {
				%s
			}
""" % s


ERRS = {
    'le_scope': a.ERRS['ok_le'],
    'lt_scope': a.ERRS['ok_lt'],
    'le_flat': """			if (dumpDir) {
				int ok;

				r = writeImage(xb.outName);
				ok = !r;
				if (ok <= 0)
					%s
				log_printf(0, separator);
			}
""" % E,
    'le_init': """			if (dumpDir) {
				int r = writeImage(xb.outName);
				int ok = !r;

				if (ok <= 0)
					%s
				log_printf(0, separator);
			}
""" % E,
    'lt_init': """			if (dumpDir) {
				int r = writeImage(xb.outName);
				int ok = r == 0;

				if (ok < 1)
					%s
				log_printf(0, separator);
			}
""" % E,
}
vs = []
for (sk, sv), (ek, ev), (ik, iv), (rk, rv) in itertools.product(SIG.items(), ERRS.items(), a.IPS.items(), a.REB.items()):
    s = a.build(a.HEAD, rv, ev, iv)
    t = gen14.split(s, sv[0], sv[1])
    if 'int r = writeImage' in t:
        t = t.replace('{\n\tint r;\n\n\tnetUnmount', '{\n\tnetUnmount')
    vs.append(('%s_%s_%s_%s' % (sk, ek, ik, rk), t))
print(len(vs))
res = sw.run(vs, '-O3', save='gen15', top=0, quiet=True)
for r in res:
    if r[1] == 0:
        print(r[0], 'SAME' if r[3] else 'not-same')
print(sorted(set(r[1] for r in res))[:10])
