"""Attempt 49: code the two loaders share as helpers both call (case 25's xell search, the
CF/CG fallback, case 24's file), scored with console's precheck and cold label (`L` rows) and
without (`n` rows).  python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a49_share.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a49_con import BASE, strip, SH

XELL_OLD = '''				if (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)
					break;
				if (!loadBaseFile(e->name, e))
					break;
				log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\\n");
				if (!loadBinFile(e))
					break;
				log_printf(1, "xell not found in firmware /bin folder, checking base path\\n");
				r = loadLocalFile(e);
				break;
'''
XELL_H = {
 'x1': '''/* xell: the perbuild directory, then the firmware /bin folder, then the base path */
static int loadXell(struct fileent *e)
{
	if (!loadBaseFile(e->name, e))
		return 0;
	log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\\n");
	if (!loadBinFile(e))
		return 0;
	log_printf(1, "xell not found in firmware /bin folder, checking base path\\n");
	return loadLocalFile(e);
}

''',
 'x2': '''/* xell: the perbuild directory, then the firmware /bin folder, then the base path */
static int loadXell(struct fileent *e)
{
	if (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)
		return 0;
	if (!loadBaseFile(e->name, e))
		return 0;
	log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\\n");
	if (!loadBinFile(e))
		return 0;
	log_printf(1, "xell not found in firmware /bin folder, checking base path\\n");
	return loadLocalFile(e);
}

''',
}
XELL_USE = {
 'x1': '''				if (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)
					break;
				r = loadXell(e);
				break;
''',
 'x2': '''				r = loadXell(e);
				break;
''',
}
CF_LB = '''				if (r) {
					if (type == 9) {
						if (suGetCF(&e->data, &e->size))
							r = 0;
					} else if (__builtin_expect(type == 10, 0)) {
						if (suGetCG(&e->data, &e->size))
							r = 0;
					}
				}
'''
CF_CO = CF_LB.replace('__builtin_expect(type == 10, 0)', 'type == 10')
CF_H = '''/* a CF or CG that isn't in the directory: the one from the update, if any */
static uint32_t suFallback(struct fileent *e, int type)
{
	if (type == 9) {
		if (suGetCF(&e->data, &e->size))
			return 0;
	} else if (type == 10) {
		if (suGetCG(&e->data, &e->size))
			return 0;
	}
	return 1;
}

'''
CF_USE = '''				if (r)
					r = suFallback(e, type);
'''
ANCHOR = '/* load the input files by their type;'


def mk(xell=None, cf=False, b24=False, keep=False):
    def f(t):
        if not keep:
            t = strip(t)
        pre = ''
        if xell:
            assert t.count(XELL_OLD) == 2
            t = t.replace(XELL_OLD, XELL_USE[xell])
            pre += XELL_H[xell]
        if cf:
            assert CF_LB in t and CF_CO in t
            t = t.replace(CF_LB, CF_USE, 1).replace(CF_CO, CF_USE, 1)
            pre += CF_H
        if b24:
            pre += SH
            o1 = '''				if (xb.type == BUILD_JTAG || xb.glitch2mfg) {
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
				}'''
            o2 = '''				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;'''
            t = t.replace(o1, '\t\t\t\tif (xb.type == BUILD_JTAG || xb.glitch2mfg)\n\t\t\t\t\tr = loadBl24(e);', 1)
            t = t.replace(o2, '\t\t\t\tif (xb.glitch2mfg)\n\t\t\t\t\tr = loadBl24(e);\n\t\t\t\tbreak;', 1)
        return t.replace(ANCHOR, pre + ANCHOR, 1)
    return f


V = {}
for keep in (False, True):
    p = 'L' if keep else 'n'
    for x in (None, 'x1', 'x2'):
        for cf in (False, True):
            for b in (False, True):
                if not (x or cf or b):
                    continue
                V['%s_%s%s%s' % (p, x or '-', '_cf' if cf else '', '_24' if b else '')] = mk(x, cf, b, keep)
