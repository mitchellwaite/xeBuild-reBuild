"""gen11.py: test that survives inlining's frequency rebuild (TODO_rebuild_frequencies after inline_transform) and folds later, between buildImage and `if (!ret)`.
Target r in [.84,.947] so block 105 becomes key 8.
 stat_ptr: static char * with initializer, never written (ipa-reference, ccp2 folds): PRED_POINTER + early return.
 stat_int: static int never written, compared to 1 with a guarded log.
 code_*:   int code = 0 in mode_update, *pret read after buildImage (FRE folds after inlining)."""
import itertools

import axes as a
import sw

CODE_OLD = """	int i, ret, code;
"""
HEAD = a.HEAD
LOGX = 'log_printf(1, "skipping\\n");'


def top(t):
    return """	int ret, r;

	if (getConsoleFiles(dumpDir)) {
		updating = 1;
		ret = buildImage();
%s		if (!ret) {
""" % t


T = {
    'stat_ptr': ('static char *mountName = "usv";\n', top("""		if (!mountName)
			return;
"""), False),
    'stat_ptr2': ('static char *imageName = "image";\n', top("""		if (!imageName)
			return;
"""), False),
    'stat_int_ret': ('static int skipFlash;\n', top("""		if (skipFlash == 1) {
			%s
			return;
		}
""" % LOGX), False),
    'stat_int_log': ('static int skipFlash;\n', top("""		if (skipFlash == 1)
			%s
""" % LOGX), False),
    'stat_int_lt': ('static int skipFlash;\n', top("""		if (skipFlash < 0) {
			%s
			return;
		}
""" % LOGX), False),
    'code_eq_ret': ('', top("""		if (*pret == 1) {
			%s
			return;
		}
""" % LOGX), True),
    'code_eq_log': ('', top("""		if (*pret == 1)
			%s
""" % LOGX), True),
    'code_lt_ret': ('', top("""		if (*pret < 0) {
			%s
			return;
		}
""" % LOGX), True),
}
RB = {k: a.REB[k] for k in ('plain', 'x_gt')}
ER = {k: a.ERRS[k] for k in ('plain', 'ok_le')}
vs = []
HAT = 'static void updateNand(char *dumpDir, int *pret)\n'
for (tk, (decl, tv, code)), (rk, rv), (ek, ev), (ik, iv) in itertools.product(T.items(), RB.items(), ER.items(), a.IPS.items()):
    s = a.build(tv, rv, ev, iv)
    s = s.replace(HAT, decl + HAT)
    if code:
        assert 'ret, code;' in s
        s = s.replace('int i, ret, code;', 'int i, ret, code = 0;')
    vs.append(('%s_%s_%s_%s' % (tk, rk, ek, ik), s))
print(len(vs))
sw.run(vs, '-O3', save='gen11', top=25)
