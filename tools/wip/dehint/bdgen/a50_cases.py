"""Attempt 50: helpers shared between loadBlFiles' own cases: case 1 / 22 (a bin-dir file or the
built-in payload / core) as one helper, case 3 / 4 (the keyvault chains) as one helper; each with
the hints off one at a time.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a50_cases.py [-p 95,99]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub, OFF, ANCHOR

BASE = H.BASE
I = '\t\t\t'


def builtin_old(what, name, size, words):
    return ('\t\t\tcase %d:\n\t\t\t\tif (!loadBinFile(e))\n\t\t\t\t\tbreak;\n'
            '\t\t\t\tlog_printf(1, "could not read %%s%%s, using built in %s (0x%%x bytes)\\n", xb.binDir, e->name, 0x%x);\n'
            '\t\t\t\te->data = malloc(0x%x);\n\t\t\t\tif (!e->data) {\n\t\t\t\t\tr = 1;\n\t\t\t\t\tbreak;\n\t\t\t\t}\n'
            '\t\t\t\te->size = 0x%x;\n\t\t\t\tmemcpy(e->data, %s, 0x%x);\n\t\t\t\tbreak;\n') % (words, what, size, size, size, name, size)


C1 = builtin_old('payload', 'defPayload', 0x200, 1)
C22 = builtin_old('core', 'defCore', 0xd40, 22)
FN_B = '''/* a file from the bin dir, else the built-in copy */
static int loadBuiltIn(struct fileent *e, const char *fmt, const uint8_t *data, uint32_t size)
{
	if (!loadBinFile(e))
		return 0;
	log_printf(1, fmt, xb.binDir, e->name, size);
	e->data = malloc(size);
	if (!e->data)
		return 1;
	e->size = size;
	memcpy(e->data, data, size);
	return 0;
}

'''


def builtin_new(n, what, name, size):
    return ('\t\t\tcase %d:\n\t\t\t\tr = loadBuiltIn(e, "could not read %%s%%s, using built in %s (0x%%x bytes)\\n", %s, 0x%x);\n'
            '\t\t\t\tbreak;\n') % (n, what, name, size)


def kv_old(n, f1, f2, fld):
    S = '&xb.files[xb.nFlashFiles]'
    return ('\t\t\tcase %d:\n\t\t\t\tif (!loadBaseFile(e->name, %s) ||\n\t\t\t\t    !loadBaseFile("%s", %s) ||\n'
            '\t\t\t\t    !(r = loadBaseFile("%s", %s))) {\n' % (n, S, f1, S, f2, S))


FN_K = '''/* a keyvault: the name, then the two default names, else the one from the nand dump */
static uint32_t loadKv(struct fileent *e, const char *name1, const char *name2, struct netfile *nand)
{
	uint32_t r = 0;

	if (!loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) ||
	    !loadBaseFile(name1, &xb.files[xb.nFlashFiles]) ||
	    !(r = loadBaseFile(name2, &xb.files[xb.nFlashFiles]))) {
		if (e->data)
			free(e->data);
		e->data = xb.files[xb.nFlashFiles].data;
		e->size = xb.files[xb.nFlashFiles].size;
		xb.files[xb.nFlashFiles].data = NULL;
		xb.files[xb.nFlashFiles].size = 0;
	} else if (nand->data) {
		log_printf(1, "reading %s%s failed, using %s from nand dump\\n", xb.baseDir, e->name, e->name);
		if (e->data)
			free(e->data);
		e->data = nand->data;
		e->size = nand->size;
		nand->data = NULL;
		nand->size = 0;
		r = 0;
	}
	return r;
}

'''


def kv_span(t, n):
    a = t.index('\t\t\tcase %d:\n\t\t\t\tif (!loadBaseFile(e->name, &xb.files' % n)
    b = t.index('\t\t\t\tbreak;\n', a) + len('\t\t\t\tbreak;\n')
    return a, b


def mk(hs):
    def f(t):
        fns = ''
        if 'b' in hs:
            fns += FN_B
            t = sub(t, C1, builtin_new(1, 'payload', 'defPayload', 0x200))
            t = sub(t, C22, builtin_new(22, 'core', 'defCore', 0xd40))
        if 'k' in hs:
            fns += FN_K
            for n, a1, a2, fld in ((3, 'keyvault.bin', 'KV_dec.bin', 'kv'), (4, 'keyvault_alt.bin', 'KV_alt_dec.bin', 'kvAlt')):
                a, b = kv_span(t, n)
                t = t[:a] + '\t\t\tcase %d:\n\t\t\t\tr = loadKv(e, "%s", "%s", &xb.%s);\n\t\t\t\tbreak;\n' % (n, a1, a2, fld) + t[b:]
        return sub(t, ANCHOR, fns + ANCHOR)
    return f


V = {}
for hs in ('b', 'k', 'bk'):
    for k in os.environ.get('A50_OFF', 'all,pr,bar,lab,none').split(','):
        def g(t, hs=hs, p=OFF[k]):
            t = mk(hs)(t)
            for a, c in p:
                t = sub(t, a, c)
            return t
        V[hs + '_' + k] = g
