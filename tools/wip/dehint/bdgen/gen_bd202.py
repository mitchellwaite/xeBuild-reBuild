"""Attempt 9, reconstruction C: gen_bd200's switch moved into `static int loadBl(e, i)`, r a local of the
helper and its return value, the loop only calling it.  No hints.  Axes as gen_bd200's (the ones that
mattered there), plus the helper's signature and how the loop calls it."""
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
CALL		if (r) {
			log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
			return -1;
		}
	}
	return 0;
}

'''
CALLS = {
    'r0': '''		r = 0;
		if (strnicmp(e->name, "none", 4) || e->crc)
			r = loadBl(e, i);
''',
    'else': '''		if (strnicmp(e->name, "none", 4) || e->crc)
			r = loadBl(e, i);
		else
			r = 0;
''',
}
# the none test inside the helper
CALL_IN = '''		r = loadBl(e, i);
'''


def helper(base, call, rtype, inner, **kw):
    t = g.make(base, rtype=rtype, **kw)
    i = t.index('int loadBlFiles(void)\n')
    j = t.index('int loadConsoleBlFiles(void)')
    body = t[i:j]
    a = body.index('\t\t\tint type = e->type;\n')
    b = body.index('\t\tif (r) {\n\t\t\tlog_printf(0, "\\n\\n**** could not read')
    sw = body[a:b]
    # sw is "int type..; switch {..}\n\t\t}\n" : drop the closing brace of the none test
    sw = sw[:sw.rindex('\t\t}\n')]
    if inner:
        head = '''/* load the input file e (xb.files[i]) by its type */
static int loadBl(struct fileent *e, uint32_t i)
{
	int r = 0;
	int type;

	if (!strnicmp(e->name, "none", 4) && !e->crc)
		return 0;
	type = e->type;
'''
        sw = sw.replace('\t\t\tint type = e->type;\n', '')
        call_text = CALL_IN
    else:
        head = '''/* load the input file e (xb.files[i]) by its type */
static int loadBl(struct fileent *e, uint32_t i)
{
	int r = 0;
'''
        call_text = CALLS[call]
    fn = head + sw + '\treturn r;\n}\n\n'
    loop = LOOP.replace('RTYPE', rtype).replace('CALL', call_text)
    return t[:i] + fn + loop + t[j:]


def CASES(base):
    out = []
    for fb, order, sig, call, rtype, inner in itertools.product(['con2', 'and'], ['5_17_11', '17_5_11'], ['N', 'L', 'P'],
                                                                ['r0', 'else'], ['int', 'uint32_t'], [0, 1]):
        if inner and call != 'r0':
            continue
        kw = dict(fb=fb, order=order, sig=sig, tail='and', guard='nest', size='else')
        out.append(('%s %s %s %s %s %s' % (fb, order, sig, 'in' if inner else call, rtype, ''),
                    lambda b, kw=kw, call=call, rtype=rtype, inner=inner: helper(b, call, rtype, inner, **kw)))
    return out


FOCUS = ['_loadBlFiles']
