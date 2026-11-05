"""The passed log behind a later test of *pr instead of `else if (type)`: PRED_CALL then only guards the failed arm (71%).  Also r-style forms."""
import importlib.util, itertools, os
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g161', os.path.join(d, 'gen_bd161.py'))
g1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g1)
g = g1.g

NEW = {
    's1': '''if (xb.pub1bl) {
	if (!cbVerifySig(e->data, xb.pub1bl)) {
		FAILED
	}
	if (!*pr)
		PASSED
} else
	NOKEY
''',
    's2': '''if (xb.pub1bl) {
	if (!cbVerifySig(e->data, xb.pub1bl))
		*pr = -1;
	if (*pr)
		LOGF
	else
		PASSED
} else
	NOKEY
''',
    's3': '''if (xb.pub1bl) {
	if (!cbVerifySig(e->data, xb.pub1bl))
		*pr = -1;
	if (!*pr)
		PASSED
	else
		LOGF
} else
	NOKEY
''',
    's4': '''if (!xb.pub1bl)
	NOKEY
else {
	if (!cbVerifySig(e->data, xb.pub1bl)) {
		FAILED
	}
	if (!*pr)
		PASSED
}
''',
    's5': '''if (xb.pub1bl) {
	if (!cbVerifySig(e->data, xb.pub1bl)) {
		FAILED
	}
	if (*pr == 0)
		PASSED
} else
	NOKEY
''',
    's6': '''if (xb.pub1bl) {
	if (!cbVerifySig(e->data, xb.pub1bl)) {
		LOGF
		*pr = -1;
		goto sigdone;
	}
	PASSED
sigdone:;
} else
	NOKEY
''',
}
g.SIGS.update(NEW)
g.TXT['LOGF'] = 'log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);'
NEWS = list(NEW) + ['dead']


def CASES(base):
    out = []
    for sg, tl, n, t10, bad, cp in itertools.product(NEWS, g1.TAILS, (0, 1), (0, 1), (0, 1), (0, 1)):
        def mk(b, sg=sg, tl=tl, n=n, t10=t10, bad=bad, cp=cp):
            t = g.with_arm(b, g.arm(sg, tl, n, t10))
            if not cp:
                t = g.nocp(t)
            return g.nobad(t) if bad else t
        out.append(('%s %s n%d t%d bad%d cp%d' % (sg, tl, n, t10, bad, cp), mk))
    return out


FOCUS = ['_loadBlFiles']
