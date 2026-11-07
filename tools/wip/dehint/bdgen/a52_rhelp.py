"""Attempt 52: retail's bootloader end (the four sums and the xell room test, which holds a log call so
einline leaves it to IPA) as a helper called at retail's start: attempt 37's route wants a retail head
that isn't the findFileOffset(5) loop header at ch2 with loads numbered above the loops' i.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a52_rhelp.py"""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
import a52_cba as C
import a52_xell as X
BASE = H.BASE
SUMS = '''		size = findFileOffset(5) + findFileSize(5);
		size += findFileSize(6);
		size += findFileSize(7);
		size += findFileSize(8);
'''
HELP = {
 'r1': '''/* where the retail and glitch bootloaders end, xell included */
static uint32_t retailBlEnd(void)
{
	uint32_t size, xs;
	int x;

	size = findFileOffset(5) + findFileSize(5);
	size += findFileSize(6);
	size += findFileSize(7);
	size += findFileSize(8);
	if (xb.type != BUILD_RETAIL) {
		x = findFile(25);
		if (xb.files[x].offset > size) {
			xs = xb.files[x].size;
			if (xs > 0x40000)
				log_printf(0, WARN);
			else
				xs = 0x40000;
			size = xb.files[x].offset + xs;
		}
	}
	return size;
}

''',
 'r2': '''/* where the retail and glitch bootloaders end, xell included */
static uint32_t retailBlEnd(void)
{
	uint32_t size, xs;
	int x;

	size = findFileOffset(5) + findFileSize(5);
	size += findFileSize(6);
	size += findFileSize(7);
	size += findFileSize(8);
	if (xb.type == BUILD_RETAIL)
		return size;
	x = findFile(25);
	if (xb.files[x].offset <= size)
		return size;
	xs = xb.files[x].size;
	if (xs > 0x40000)
		log_printf(0, WARN);
	else
		xs = 0x40000;
	return xb.files[x].offset + xs;
}

''',
}
V = {}
for h, pin in itertools.product(HELP, (1, 0)):
    def f(t, h=h, pin=pin):
        if not pin:
            t = t.replace(H.PIN[0], '', 1)
        for a in (SUMS + X.OLD,):
            if a not in t:
                raise ValueError('old')
            t = t.replace(a, '\t\tsize = retailBlEnd();\n', 1)
        return t.replace(C.HEAD, HELP[h].replace('WARN', X.WARN) + C.HEAD, 1)
    V['%s_%s' % (h, 'P' if pin else 'n')] = f
