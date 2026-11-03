"""gen12.py: the dead test on the success edge only, with a goto into the buildImage error arm: 105 scaled down, 128 raised."""
import itertools

import axes as a
import cur2
import sw

FATAL_OLD = """		} else {
			log_printf(0, "\\n\\n***** FATAL UPDATE ERROR: %i unable to complete NAND image\\n\\n", ret);
"""
FATAL_NEW = """		} else {
		fatal:
			log_printf(0, "\\n\\n***** FATAL UPDATE ERROR: %i unable to complete NAND image\\n\\n", ret);
"""


def top(t):
    return """	int ret, r;

	if (getConsoleFiles(dumpDir)) {
		updating = 1;
		ret = buildImage();
		if (!ret) {
%s""" % t


T = {
    'ptr': ('static char *mountName = "usv";\n', top("""			if (!mountName)
				goto fatal;
"""), False),
    'int1': ('static int skipFlash;\n', top("""			if (skipFlash == 1)
				goto fatal;
"""), False),
    'intlt': ('static int skipFlash;\n', top("""			if (skipFlash < 0)
				goto fatal;
"""), False),
    'int0': ('static int skipFlash;\n', top("""			if (skipFlash)
				goto fatal;
"""), False),
    'c1': ('', top("""			if (*pret == 1)
				goto fatal;
"""), True),
    'clt': ('', top("""			if (*pret < 0)
				goto fatal;
"""), True),
}
RB = {k: a.REB[k] for k in ('plain', 'x_gt')}
ER = {k: a.ERRS[k] for k in ('plain', 'ok_le')}
vs = []
HAT = 'static void updateNand(char *dumpDir, int *pret)\n'
for (tk, (decl, tv, code)), (rk, rv), (ek, ev), (ik, iv) in itertools.product(T.items(), RB.items(), ER.items(), a.IPS.items()):
    s = a.build(tv, rv, ev, iv)
    assert FATAL_OLD in s
    s = s.replace(FATAL_OLD, FATAL_NEW)
    s = s.replace(HAT, decl + HAT)
    if code:
        s = s.replace('int i, ret, code;', 'int i, ret, code = 0;')
    vs.append(('%s_%s_%s_%s' % (tk, rk, ek, ik), s))
print(len(vs))
sw.run(vs, '-O3', save='gen12', top=25)
