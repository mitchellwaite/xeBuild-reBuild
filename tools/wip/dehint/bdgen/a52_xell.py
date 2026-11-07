"""Attempt 52: calcBlAreaSize's xell room test as a helper (it holds a log call, so einline leaves it to
IPA: fresh SSA names and its own profile), with pin_size on ('P') and off ('n'), alone or with
a52_cba's addCfArea.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a52_xell.py"""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
import a52_cba as C
BASE = H.BASE
OLD = '''		if (xb.type != BUILD_RETAIL) {
			x = findFile(25);
			if (xb.files[x].offset > size) {
				xs = xb.files[x].size;
				if (xs > 0x40000)
					log_printf(0, "***** WARNING: xell is unexpectedly larger than 256KiB!!\\n");
				else
					xs = 0x40000;
				size = xb.files[x].offset + xs;
			}
		}
'''
WARN = '"***** WARNING: xell is unexpectedly larger than 256KiB!!\\n"'
HELP = {
 'a': '''/* xell goes at its own offset, with at least 256KiB of room */
static uint32_t xellEnd(uint32_t size)
{
	uint32_t xs;
	int x = findFile(25);

	if (xb.files[x].offset > size) {
		xs = xb.files[x].size;
		if (xs > 0x40000)
			log_printf(0, WARN);
		else
			xs = 0x40000;
		size = xb.files[x].offset + xs;
	}
	return size;
}

''',
 'b': '''/* xell goes at its own offset, with at least 256KiB of room */
static uint32_t xellEnd(uint32_t size)
{
	struct fileent *e = &xb.files[findFile(25)];
	uint32_t xs;

	if (e->offset <= size)
		return size;
	xs = e->size;
	if (xs > 0x40000)
		log_printf(0, WARN);
	else
		xs = 0x40000;
	return e->offset + xs;
}

''',
 'c': '''/* xell goes at its own offset, with at least 256KiB of room */
static uint32_t xellEnd(uint32_t size)
{
	uint32_t xs;
	int x = findFile(25);

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
CALL = {
 'i': '		if (xb.type != BUILD_RETAIL)\n			size = xellEnd(size);\n',
}
V = {}
for h, slot, pin in itertools.product(HELP, (0, 1), (1, 0)):
    def f(t, h=h, slot=slot, pin=pin):
        if slot:
            t = C.mk('slot', pin)(t)
        elif not pin:
            t = t.replace(H.PIN[0], '', 1)
        if OLD not in t:
            raise ValueError('old')
        t = t.replace(OLD, CALL['i'], 1)
        return t.replace(C.HEAD, HELP[h].replace('WARN', WARN) + C.HEAD, 1)
    V['%s%s_%s' % (h, '_slot' if slot else '', 'P' if pin else 'n')] = f
