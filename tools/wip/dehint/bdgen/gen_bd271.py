"""Attempt 16, pin_d: address spellings in loadBl's case 27, pin off.  `xb.files + xb.nFlashFiles` is a
POINTER_PLUS in GIMPLE where `&xb.files[xb.nFlashFiles]` is an ARRAY_REF address, which changes what PRE and
IRA see (the lever that replaced XB_PATCHES in mode_update).  IRA (attempt 16) pops the base's thread
(r535 = r534 + xb, r534 = n * 0x42c) before d and before n (pretmp_80, edx), so the base takes eax.
Axes: the spelling at the three loadBaseFile calls (a), in the fallback arm (f), at the d/size reads (d).
Runs on src/build.c as of e76f027f."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

OLD = '''		if (loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) &&
		    loadBaseFile("config.bin", &xb.files[xb.nFlashFiles]) &&
		    (*pr = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]))) {
			if (!xb.smcConfig.data)
				break;
			log_printf(1, "reading %s%s failed, using %s from nand dump\\n", xb.baseDir, e->name, e->name);
			if (xb.files[xb.nFlashFiles].data)
				free(xb.files[xb.nFlashFiles].data);
			xb.files[xb.nFlashFiles].data = xb.smcConfig.data;
			xb.smcConfig.data = NULL;
			xb.files[xb.nFlashFiles].size = xb.smcConfig.size;
			xb.smcConfig.size = 0;
			*pr = 0;
		}
		{
			uint8_t *d = xb.files[xb.nFlashFiles].data;

			if (d)
				*pr = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);
		}
		break;
'''
A = {'arr': '&xb.files[xb.nFlashFiles]', 'add': 'xb.files + xb.nFlashFiles'}
F = {'arr': 'xb.files[xb.nFlashFiles].', 'add': '(xb.files + xb.nFlashFiles)->'}
D = {
    'arr': '''		{
			uint8_t *d = xb.files[xb.nFlashFiles].data;

			if (d)
				*pr = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);
		}
''',
    'add': '''		{
			uint8_t *d = (xb.files + xb.nFlashFiles)->data;

			if (d)
				*pr = extractSmcConfig(e, d, (xb.files + xb.nFlashFiles)->size);
		}
''',
    'ptr': '''		{
			struct fileent *c = xb.files + xb.nFlashFiles;

			if (c->data)
				*pr = extractSmcConfig(e, c->data, c->size);
		}
''',
    'plain': '''		if ((xb.files + xb.nFlashFiles)->data)
			*pr = extractSmcConfig(e, (xb.files + xb.nFlashFiles)->data, (xb.files + xb.nFlashFiles)->size);
''',
}


def mk(t, a, f, d):
    s = OLD[:OLD.index('		{\n			uint8_t *d')]
    s = s.replace('&xb.files[xb.nFlashFiles]', A[a]).replace('xb.files[xb.nFlashFiles].', F[f])
    s += D[d] + '		break;\n'
    return bdrun.sub(t, OLD, s, 1)


def CASES(base):
    t0 = bdhints.off(base, 'pin_d')
    out = []
    for a, f, d in itertools.product(A, F, D):
        out.append(('%s %s %s' % (a, f, d), mk(t0, a, f, d)))
    return out


FOCUS = ['_loadBlFiles']
