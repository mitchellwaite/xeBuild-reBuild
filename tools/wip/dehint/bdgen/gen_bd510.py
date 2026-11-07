"""Attempt 39: how the data reaches loadBl (interface level, not per-hint spellings), crossed with every loadBl-side
trick off alone.  Variants: loadBl takes i and computes e itself (`iarg`), the tail reads e->data instead of
xb.files[i].data (`edata`), the loop's r / e declared in the loop body (`rscope`, `escope`: a scoped address-taken r
gets a CLOBBER at the end of each iteration), a pointer IV in the loop (`eptr`), the "none" skip test moved into
loadBl as an early return (`noneinbl`), case 2's slot through a local pointer (`c2slot`).  Runs on src as of a9cb46e0.
`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd510.py`."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdhints, bdrun

FOCUS = ['_loadBlFiles']

LB_HEAD = 'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)\n{\n\tint type;\n'
LOOP = '''	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		e = &xb.files[i];
		r = 0;
		if (strnicmp(e->name, "none", 4) || e->crc)
			loadBl(e, i, &r);
		if (r) {'''


def lbf(t, old, new):
    a, b = bdrun.fnspan(t, 'int loadBlFiles(void)')
    s = t[a:b]
    if old not in s:
        raise ValueError('lbf: ' + old[:50])
    return t[:a] + s.replace(old, new, 1) + t[b:]


def iarg(t):
    t = bdrun.sub(t, LB_HEAD, 'static void loadBl(uint32_t i, uint32_t *pr)\n{\n\tstruct fileent *e = &xb.files[i];\n\tint type;\n', 1)
    return lbf(t, 'loadBl(e, i, &r);', 'loadBl(i, &r);')


def edata(t):
    return bdrun.sub(t, 'setFlashBuild(getBeU16(xb.files[i].data + 2));', 'setFlashBuild(getBeU16(e->data + 2));', 1)


def rscope(t):
    t = lbf(t, '\tuint32_t r;\n\n', '\n')
    return lbf(t, '\t\tr = 0;\n', '\t\tuint32_t r = 0;\n\n')


def escope(t):
    t = lbf(t, '\tstruct fileent *e;\n\tuint32_t i;\n\tuint32_t r;\n', '\tuint32_t i;\n')
    return lbf(t, '\t\te = &xb.files[i];\n\t\tr = 0;\n', '\t\tstruct fileent *e = &xb.files[i];\n\t\tuint32_t r = 0;\n\n')


def eptr(t):
    t = lbf(t, 'for (i = 1; i < (uint32_t)xb.nFiles; i++) {\n\t\te = &xb.files[i];\n',
            'for (i = 1, e = &xb.files[1]; i < (uint32_t)xb.nFiles; i++, e++) {\n')
    return t


def noneinbl(t):
    t = bdrun.sub(t, LB_HEAD + '\n\ttype = e->type;\n',
                  LB_HEAD + '\n\tif (!strnicmp(e->name, "none", 4) && !e->crc)\n\t\treturn;\n\ttype = e->type;\n', 1)
    return lbf(t, '\t\tif (strnicmp(e->name, "none", 4) || e->crc)\n\t\t\tloadBl(e, i, &r);\n', '\t\tloadBl(e, i, &r);\n')


C2 = '''	case 2:
		*pr = loadBaseFile(e->name, &xb.files[xb.nFlashFiles]);
		if (!*pr) {
			if (e->data)
				free(e->data);
			e->data = xb.files[xb.nFlashFiles].data;
			e->size = xb.files[xb.nFlashFiles].size;
			xb.files[xb.nFlashFiles].data = NULL;
			xb.files[xb.nFlashFiles].size = 0;
'''


def c2slot(t):
    new = '''	case 2: {
		struct fileent *f = &xb.files[xb.nFlashFiles];

		*pr = loadBaseFile(e->name, f);
		if (!*pr) {
			if (e->data)
				free(e->data);
			e->data = f->data;
			e->size = f->size;
			f->data = NULL;
			f->size = 0;
'''
    t = bdrun.sub(t, C2, new, 1)
    return bdrun.sub(t, '\t\tif (!e->offset)\n\t\t\tgoto fail;\n\t\tbreak;\n\tdefault:', '\t\tif (!e->offset)\n\t\t\tgoto fail;\n\t\tbreak;\n\t}\n\tdefault:', 1)


VARIANTS = {
    'src': lambda t: t,
    'iarg': iarg,
    'edata': edata,
    'rscope': rscope,
    'escope': escope,
    'eptr': eptr,
    'noneinbl': noneinbl,
    'noneinbl+iarg': lambda t: iarg(noneinbl(t)),
    'c2slot': c2slot,
    'iarg+escope': lambda t: iarg(lbf(lbf(t, '\tstruct fileent *e;\n\tuint32_t i;\n\tuint32_t r;\n', '\tstruct fileent *e;\n\tuint32_t i;\n'),
                                      '\t\tr = 0;\n', '\t\tuint32_t r = 0;\n\n')),
}

ETYPE = ('\t\t\t\t} else if (type)\n', '\t\t\t\t} else\n')
CP = ('if ((char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1) {',
      'if (0) {')


def off(t, k):
    if k == 'none':
        return t
    if k == 'etype':
        return bdrun.sub(t, *ETYPE)
    if k == 'cp':
        return bdrun.sub(t, *CP)
    return bdhints.off(t, k)


OFFS = os.environ.get('BDOFFS', 'none,exp_t10,exp_pr,lab_t5le,vol_fail,lab_none,etype,cp').split(',')


def CASES(base):
    out = []
    for v, f in VARIANTS.items():
        for k in OFFS:
            out.append(('%s|%s' % (v, k), lambda b, f=f, k=k: off(f(b), k)))
    return out
