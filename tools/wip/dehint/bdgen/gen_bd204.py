"""Attempt 9, reconstruction B2: gen_bd200's switch (A's arms) in `static void loadBl(e, i, pr)`, called from
the loop as src does (`r = 0; if (none test) loadBl(e, i, &r);`).  The call in the guarded block is what
gives the none test src's 29% (PRED_CALL, while the helper is still a call at profile_estimate); A's
inlined switch gets 50% and so the case arms are too hot (597 against 513) and cases 2 and 27 move.
A helper returning r (gen_bd202) gets that right but its `return r` puts return predictors on the arms.
No hints.  Axes: r through *pr or a local stored at the end, A's arm axes."""
import importlib.util, itertools, os
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g200', os.path.join(d, 'gen_bd200.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

LOOP = '''int loadBlFiles(void)
{
	struct fileent *e;
	uint32_t i;
	RTYPE r;

	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		e = &xb.files[i];
		r = 0;
		if (strnicmp(e->name, "none", 4) || e->crc)
			loadBl(e, i, &r);
		if (r) {
			log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
			return -1;
		}
	}
	return 0;
}

'''


def helper(base, mode, rtype, **kw):
    t = g.make(base, rtype=rtype, **kw)
    i = t.index('int loadBlFiles(void)\n')
    j = t.index('int loadConsoleBlFiles(void)')
    body = t[i:j]
    a = body.index('\t\t\tint type = e->type;\n')
    b = body.index('\t\tif (r) {\n\t\t\tlog_printf(0, "\\n\\n**** could not read')
    sw = body[a:b]
    sw = sw[:sw.rindex('\t\t}\n')]
    if mode == 'pr':
        import re
        sw = re.sub(r'\br\b', '*pr', sw)
        head = '/* load the input file e (xb.files[i]) by its type */\nstatic void loadBl(struct fileent *e, uint32_t i, RTYPE *pr)\n{\n'
        fn = head + sw + '}\n\n'
    else:
        head = '/* load the input file e (xb.files[i]) by its type */\nstatic void loadBl(struct fileent *e, uint32_t i, RTYPE *pr)\n{\n\tRTYPE r = 0;\n\n'
        fn = head + sw + '\t*pr = r;\n}\n\n'
    fn = fn.replace('RTYPE', rtype)
    return t[:i] + fn + LOOP.replace('RTYPE', rtype) + t[j:]


def CASES(base):
    out = []
    for mode, rtype, fb, order, sig, guard, tail in itertools.product(['pr', 'local'], ['uint32_t', 'int'], ['con2', 'and', 'con'],
                                                                       ['5_17_11', '17_5_11'], ['N', 'L', 'P'], ['nest', 'brk'], ['and']):
        kw = dict(fb=fb, order=order, sig=sig, tail=tail, guard=guard, size='else')
        out.append(('%s %s %s %s %s %s %s' % (mode, rtype, fb, order, sig, guard, tail),
                    lambda b, kw=kw, mode=mode, rtype=rtype: helper(b, mode, rtype, **kw)))
    return out


FOCUS = ['_loadBlFiles']
