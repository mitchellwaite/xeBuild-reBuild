# attempt 10: pin_hdr gone.  pageErased itself must keep its loops' 4.5% (its own code), but finalizeImage's copy needn't come from it: a static helper for finalizeImage alone,
# `pageUsed`, returns 1 for a page with data.  Forms of its two loops (plain, spareUsed, byte helper of class u or v) and of the test.  Only finalizeImage can change.
import os
PIN = '			__asm__("" :: "a"(xb.hdr));\n'
TEST = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
'''
FI = 'int finalizeImage(void)\n{\n'
ARGS = 'xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16'
BU = 'static int byteUsed(uint8_t b)\n{\n	if (b != 0xff)\n		return 1;\n	return 0;\n}\n\n'
BV = 'static int byteUsed(uint8_t b)\n{\n	if (b == 0xff)\n		return 0;\n	return 1;\n}\n\n'
D = {
 '': ('', '	for (i = 0; i < 512; i++)\n		if (data[i] != 0xff)\n			return 1;\n'),
 'Du': (BU, '	for (i = 0; i < 512; i++)\n		if (byteUsed(data[i]))\n			return 1;\n'),
 'Dv': (BV, '	for (i = 0; i < 512; i++)\n		if (byteUsed(data[i]))\n			return 1;\n'),
}
S = {
 'a': ('', '	for (i = 0; i < 16; i++)\n		if (spare[i] != 0xff)\n			return 1;\n	return 0;\n'),
 'b': ('', '	return spareUsed(spare);\n'),
 'c': ('', '	if (spareUsed(spare))\n		return 1;\n	return 0;\n'),
 'u': (BU, '	for (i = 0; i < 16; i++)\n		if (byteUsed(spare[i]))\n			return 1;\n	return 0;\n'),
 'v': (BV, '	for (i = 0; i < 16; i++)\n		if (byteUsed(spare[i]))\n			return 1;\n	return 0;\n'),
 'm': ('', '	for (i = 0; i < 16; i++)\n		if (spare[i] == 0xff)\n			continue;\n		else\n			return 1;\n	return 0;\n'),
}
V = []
for dk, (dh, db) in D.items():
    for sk, (sh, sb) in S.items():
        if dh and sh and dh != sh:
            continue
        h = dh or sh
        fn = h + 'static int pageUsed(const uint8_t *data, const uint8_t *spare)\n{\n	int i;\n\n' + db + sb + '}\n\n'
        V.append((dk + sk, [(FI, fn + FI), (TEST, '			if (pageUsed(%s))\n' % ARGS)]))
        fn2 = fn.replace('return 1;', 'return @;').replace('return 0;', 'return 1;').replace('return @;', 'return 0;').replace('pageUsed', 'pageBlank').replace('byteUsed(data[i])', 'byteUsed(data[i])')
        if 'spareUsed' not in fn2 and 'static int byteUsed' not in fn2:
            V.append((dk + sk + 'N', [(FI, fn2 + FI), (TEST, '			if (!pageBlank(%s))\n' % ARGS)]))
AXES = [
 [('nopin', [(PIN, '')])],
 V,
]
BASE = os.environ.get('IWB', 'src/image_write.c')
FLAGS = []
FOCUS = ['_finalizeImage']
