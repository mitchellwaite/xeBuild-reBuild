"""Attempt 9: edits on reconstruction A (gen_bd200's best: con2 5_17_11 N and nest else int), alone and in
pairs, to price each of A's differences.  Some put hints back (named h_*), to see which A needs."""
import importlib.util, itertools, os
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g200', os.path.join(d, 'gen_bd200.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
A = dict(fb='con2', order='5_17_11', sig='N', tail='and', guard='nest', size='else', rtype='int')


def sub(t, a, b):
    if a not in t:
        raise ValueError('not found: %r' % a[:60])
    return t.replace(a, b, 1)


C27 = '''				if (xb.files[xb.nFlashFiles].data)
					r = extractSmcConfig(e, xb.files[xb.nFlashFiles].data, xb.files[xb.nFlashFiles].size);
'''
C27D = '''				{
					uint8_t *d = xb.files[xb.nFlashFiles].data;

PIN					if (d)
						r = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);
				}
'''


def d_local(t):
    return sub(t, C27, C27D.replace('PIN', ''))


def h_dpin(t):
    return sub(t, C27, C27D.replace('PIN', '\t\t\t\t\t__asm__("" : "+a"(d));\n'))


def h_t10(t):
    return sub(t, '} else if (type == 10) {\n\t\t\t\t\t\tif (suGetCG', '} else if (__builtin_expect(type == 10, 0)) {\n\t\t\t\t\t\tif (suGetCG')


SIGFAIL = 'log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);\n\t\t\t\t\tr = -1;'
SIZEFAIL = 'is not a multiple of 4!\\n", e->size);\n\t\t\t\t\tr = -1;'
SMCFAIL = 'if (!e->offset)\n\t\t\t\t\tr = -1;'
DEFAULT = '''				log_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);
				break;
'''


def failsw(t, vol):
    t = sub(t, SIGFAIL, SIGFAIL.replace('r = -1;', 'goto fail;'))
    t = sub(t, SIZEFAIL, SIZEFAIL.replace('r = -1;', 'goto fail;'))
    t = sub(t, SMCFAIL, SMCFAIL.replace('r = -1;', 'goto fail;'))
    return sub(t, DEFAULT, DEFAULT + '\t\t\tfail:\n' + ('\t\t\t\t__asm__ __volatile__("");\n' if vol else '') + '\t\t\t\tr = -1;\n\t\t\t\tbreak;\n')


def fail(t):
    return failsw(t, 0)


def h_failvol(t):
    return failsw(t, 1)


def h_badsize(t):
    return sub(t, '\t\t\t\t\tlog_printf(1, "\\n\\n***** ERROR: patch size', '\t\t\t\tbadsize: __attribute__((hot));\n\t\t\t\t\tlog_printf(1, "\\n\\n***** ERROR: patch size')


EDITS = [d_local, h_dpin, h_t10, fail, h_failvol, h_badsize]


def CASES(base):
    a = g.make(base, **A)
    out = [('A', a)]
    for e in EDITS:
        out.append((e.__name__, lambda b, e=e: e(a)))
    for e1, e2 in itertools.combinations(EDITS, 2):
        if {e1, e2} in ({d_local, h_dpin}, {fail, h_failvol}):
            continue
        out.append((e1.__name__ + '+' + e2.__name__, lambda b, e1=e1, e2=e2: e2(e1(a))))
    out.append(('dpin+failvol+t10', lambda b: h_t10(h_failvol(h_dpin(a)))))
    out.append(('dpin+failvol+t10+badsize', lambda b: h_badsize(h_t10(h_failvol(h_dpin(a))))))
    return out


FOCUS = ['_loadBlFiles']
