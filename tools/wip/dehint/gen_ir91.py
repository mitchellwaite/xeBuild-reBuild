"""getImageSmc: the size arm as a static helper: a call in the arm's first block at profile_estimate if it isn't early-inlined.  Other hints kept or not."""
FOCUS = ['_getImageSmc']
BASE = 'src/image_read.c'
ATTR = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc'
HELP = '''static int fixSmcSize(int addr)
{
	int size;

	if (addr == 0x800) {
		size = 0x3800;
		log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);
	} else {
		size = 0x3000;
		log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);
	}
	return size;
}

'''
OLD = '''	if (size != 0x3000 && size != 0x3800) {
		shot: __attribute__((hot));
		if (addr == 0x800) {
			size = 0x3800;
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);
		} else {
			size = 0x3000;
			if (!h)
				__builtin_unreachable();
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);
		}
	} else
		__asm__("" : "+D"(addr));
'''
AXES = [
    [('atk', [(ATTR, HELP + ATTR)]), ('at0', [(ATTR, HELP + 'void getImageSmc')])],
    [('pk', [(OLD, '	if (size != 0x3000 && size != 0x3800)\n		size = fixSmcSize(addr);\n	else\n		__asm__("" : "+D"(addr));\n')]),
     ('p0', [(OLD, '	if (size != 0x3000 && size != 0x3800)\n		size = fixSmcSize(addr);\n')])],
    [('ek', []), ('e0', [('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {', 'if (addr < 528 * xb.dumpPages) {')])],
]
