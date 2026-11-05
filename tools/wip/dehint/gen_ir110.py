"""getImageSmc: one bad-address arm, as the Linux build shows (`test; je L; lea; test; jne L`, one log), other hints kept or not: is the reference's `mov [esp+8],0; jmp` then DOM/uncprop's copy?  vhot gone at least?"""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
A = '''	if (!addr) {
		log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
		addr = 0x1000;
	} else {
		vhot: __attribute__((hot));
	}
	if (addr != 0x800 && addr != 0x1000)
		goto bad;
'''
ATTR = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc'
BH = '	bhot: __attribute__((hot));\n'
F = {
    'or': '	if (!addr || (addr != 0x800 && addr != 0x1000))\n		goto bad;\n',
    'or2': '	if (addr == 0)\n		goto bad;\n	if (addr != 0x800 && addr != 0x1000)\n		goto bad;\n',
    'or3': '	if (!addr)\n		goto bad;\n	if (addr != 0x800) {\n		if (addr != 0x1000)\n			goto bad;\n	}\n',
    'or4': '	if (!addr)\n		goto bad;\n	else if (addr != 0x800 && addr != 0x1000)\n		goto bad;\n',
    'or5': '	if (addr) {\n		if (addr != 0x800 && addr != 0x1000)\n			goto bad;\n	} else\n		goto bad;\n',
}
SH = '		shot: __attribute__((hot));\n'
AXES = [[(k, [(A, v)]) for k, v in F.items()],
        [('bh', []), ('b0', [(BH, '')])],
        [('at', []), ('a0', [(ATTR, 'void getImageSmc')])],
        [('sh', []), ('s0', [(SH, '')])]]
