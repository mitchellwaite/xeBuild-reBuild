"""detectController, no pins, whole-function shapes (attempt 14): lba0/lba1 computed up front as in checkBlock (sink moves lba0 after the first test),
block-local structs, nested ifs, single exit, found's place and type."""
import itertools, re
FOCUS = ['_detectController']
src = open('src/image_read.c', newline='').read().replace('\r\n', '\n')
a = src.rindex('int detectController(uint8_t *raw, int size)')
b = src.rindex('int checkHeader(const char *name, FILE *fp)')
OLD = src[a:b]
SMALL0 = '''log_printf(1, "\\tNAND dump is from a small block machine\\n");
		xb.dumpBigBlock = 0;
		xb.muChecked = 1;
'''
BB = '''log_printf(1, "\\tNAND dump uses big block controller\\n");
xb.dumpBbController = 1;
'''
SB = '''log_printf(1, "\\tNAND dump uses small block controller\\n");
xb.dumpBbController = 0;
'''
SUMS = {
 # decl+tests: %(arm1)s %(arm2)s
 'hl': '''int hi, lo;
hi = (b[514] & 0xf) * 256;
lo = b[513];
if (hi + lo == i) { %(arm1)s } else { int lo2 = b[512]; if (lo2 + (b[513] & 0xf) * 256 == i) { %(arm2)s } }
''',
 'up': '''int lba0, lba1;
lba1 = b[513] + (b[514] & 0xf) * 256;
lba0 = b[512] + (b[513] & 0xf) * 256;
if (lba1 == i) { %(arm1)s } else if (lba0 == i) { %(arm2)s }
''',
 'up2': '''int lba0 = b[512] + (b[513] & 0xf) * 256;
int lba1 = b[513] + (b[514] & 0xf) * 256;
if (lba1 == i) { %(arm1)s } else if (lba0 == i) { %(arm2)s }
''',
 'upb': '''struct bigSpare *big = (struct bigSpare *)(b + 512);
struct smallSpare *s = (struct smallSpare *)(b + 512);
int lba1 = big->blockId1 + big->blockId0 * 256;
int lba0 = s->blockId1 + s->blockId0 * 256;
if (lba1 == i) { %(arm1)s } else if (lba0 == i) { %(arm2)s }
''',
 'upb2': '''struct bigSpare *big = (struct bigSpare *)(b + 512);
struct smallSpare *s = (struct smallSpare *)(b + 512);
int lba0 = s->blockId1 + s->blockId0 * 256;
int lba1 = big->blockId1 + big->blockId0 * 256;
if (lba1 == i) { %(arm1)s } else if (lba0 == i) { %(arm2)s }
''',
 'upu': '''uint32_t lba1 = b[513] + (b[514] & 0xf) * 256;
uint32_t lba0 = b[512] + (b[513] & 0xf) * 256;
if (lba1 == i) { %(arm1)s } else if (lba0 == i) { %(arm2)s }
''',
 'in': '''if (b[513] + (b[514] & 0xf) * 256 == i) { %(arm1)s } else if (b[512] + (b[513] & 0xf) * 256 == i) { %(arm2)s }
''',
 'in2': '''if (b[513] + (b[514] & 0xf) * 256 == i) { %(arm1)s } else { if (b[512] + (b[513] & 0xf) * 256 == i) { %(arm2)s } }
''',
 'ib': '''struct bigSpare *big = (struct bigSpare *)(b + 512);
struct smallSpare *s = (struct smallSpare *)(b + 512);
if (big->blockId1 + big->blockId0 * 256 == i) { %(arm1)s } else if (s->blockId1 + s->blockId0 * 256 == i) { %(arm2)s }
''',
 'm': '''uint8_t m = b[513];
int hi = (b[514] & 0xf) * 256;
if (hi + m == i) { %(arm1)s } else { int lo2 = b[512]; if (lo2 + (m & 0xf) * 256 == i) { %(arm2)s } }
''',
 'im': '''int m = b[513];
int lba1 = m + (b[514] & 0xf) * 256;
if (lba1 == i) { %(arm1)s } else { int lba0 = b[512] + (m & 0xf) * 256; if (lba0 == i) { %(arm2)s } }
''',
}
GUARD = {
 'cont': ('''if (b[517] != 0xff || b[513] == 0xff)
continue;
''', ''),
 'nest': ('''if (b[517] == 0xff) { if (b[513] != 0xff) {
''', '''} }
'''),
 'and': ('''if (b[517] == 0xff && b[513] != 0xff) {
''', '''}
'''),
 'c2': ('''if (b[517] != 0xff)
continue;
if (b[513] == 0xff)
continue;
''', ''),
}
ARM = {
 'nb': lambda arm: 'i = n;\n' + arm + 'found = 1;\n',
 'nm': lambda arm: arm + 'found = 1;\ni = n;\n',
 'fb': lambda arm: 'found = 1;\n' + arm + 'i = n;\n',
}
TOP = {
 # early returns (HEAD)
 'early': lambda loop, ft: '''int detectController(uint8_t *raw, int size)
{
	int i, n;
	%s found;

	if (size == 0x3000000) {
		log_printf(1, "\\tNAND dump is from a mmc machine\\n");
		log_printf(1, "\\tNAND dump uses big block controller\\n");
		xb.dumpBbController = 1;
		xb.dumpBigBlock = 0;
		xb.muChecked = 1;
		xb.dumpMmc = 1;
		return 1;
	}
	if (raw[512] == 0xff) {
		log_printf(1, "\\tNAND dump is from a big block machine\\n");
		log_printf(1, "\\tNAND dump uses big block controller\\n");
		if (size < 0x4200000) {
			log_printf(0, "***** WARNING: NAND dump too small to be from a big block machine, discarding dump!\\n");
			return 0;
		}
		xb.dumpBigBlock = 1;
		xb.dumpBbController = 1;
		return 1;
	}
	if (raw[517] == 0xff) {
		n = size / 16896;
		%s
		found = 0;
		%s
		return found;
	}
	log_printf(0, "***** WARNING: NAND dump does not appear to have a good block at block 0, discarding dump!\\n");
	return 0;
}

''' % (ft, SMALL0, loop),
 # single exit, found used for every return
 'single': lambda loop, ft: '''int detectController(uint8_t *raw, int size)
{
	%s found = 0;

	if (size == 0x3000000) {
		log_printf(1, "\\tNAND dump is from a mmc machine\\n");
		log_printf(1, "\\tNAND dump uses big block controller\\n");
		xb.dumpBbController = 1;
		xb.dumpBigBlock = 0;
		xb.muChecked = 1;
		xb.dumpMmc = 1;
		found = 1;
	} else if (raw[512] == 0xff) {
		log_printf(1, "\\tNAND dump is from a big block machine\\n");
		log_printf(1, "\\tNAND dump uses big block controller\\n");
		if (size < 0x4200000) {
			log_printf(0, "***** WARNING: NAND dump too small to be from a big block machine, discarding dump!\\n");
		} else {
			xb.dumpBigBlock = 1;
			xb.dumpBbController = 1;
			found = 1;
		}
	} else if (raw[517] == 0xff) {
		int i, n = size / 16896;
		%s
		%s
	} else
		log_printf(0, "***** WARNING: NAND dump does not appear to have a good block at block 0, discarding dump!\\n");
	return found;
}

''' % (ft, SMALL0, loop),
}
def loop(sums, g, arm):
    a1 = ARM[arm](BB)
    a2 = ARM[arm](SB)
    return '''for (i = 1; i < n; i++) {
uint8_t *b = raw + i * 16896;
%s%s%s}
''' % (GUARD[g][0], SUMS[sums] % {'arm1': a1, 'arm2': a2}, GUARD[g][1])
AX = []
for t, s, g, arm, ft in itertools.product(TOP, SUMS, GUARD, ARM, ['uint32_t', 'int']):
    AX.append(('.'.join((t, s, g, arm, ft[0])), [(OLD, TOP[t](loop(s, g, arm), ft))]))
AXES = [AX]
