"""patchBlsBlmod without no-early-inlining: findFile written out, for one, two or all of the three."""
import itertools
DECL = '''	int cd = findFile(7), cbb = findFile(6), pt = findFile(23);
	struct fileent *p = &xb.files[pt];
	uint8_t *d = p->data;
	uint32_t off, addr, len, i, max, end, t;
	int n = 0;

'''


def out(var, ty, form):
    if form == 'call':
        return '\t%s = findFile(%d);\n' % (var, ty)
    if form == 'for':
        return ('\t%s = 0;\n\tfor (j = 0; j < xb.nFiles; j++)\n\t\tif (xb.files[j].type == %d) {\n\t\t\t%s = j;\n\t\t\tbreak;\n\t\t}\n' % (var, ty, var))
    if form == 'self':
        return ('\tfor (%s = 0; %s < xb.nFiles; %s++)\n\t\tif (xb.files[%s].type == %d)\n\t\t\tbreak;\n\tif (%s >= xb.nFiles)\n\t\t%s = 0;\n' % (var, var, var, var, ty, var, var))


def CASES(base):
    res = []
    for a, b, c in itertools.product(('call', 'for', 'self'), repeat=3):
        new = '\tint cd, cbb, pt, j;\n\tstruct fileent *p;\n\tuint8_t *d;\n\tuint32_t off, addr, len, i, max, end, t;\n\tint n = 0;\n\n'
        new += out('cd', 7, a) + out('cbb', 6, b) + out('pt', 23, c) + '\tp = &xb.files[pt];\n\td = p->data;\n'

        def f(t, new=new):
            return t.replace(DECL, new)
        res.append(('nei_blmod', '%s-%s-%s' % (a, b, c), f))
    return res
