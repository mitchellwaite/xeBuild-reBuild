"""parseDump, signed loop: the -4 arm rejoins before `dst != blk` (threaded by VRP/DOM, the PHI's name may
survive), rem label or not; do-while form."""
FOCUS = ['_parseDump']
BASE = 'build/ir/gen_ir24_best.c'
LOOP0 = '''	for (n = 0; (int)n < blocks; n++) {
		blk = n;
		src = raw + blk * 528 * ppb;
'''
ARM = '''			dst = blk;
		} else {
rem: __attribute__((hot));
			if (dst != blk) {
				if (blk >= blocks - 32)
					log_printf(1, "copying nanddump data from block 0x%x to block 0x%x for file extraction integrity\\n", blk, dst);
				else {
					log_printf(0, "***** WARNING: ignoring possible remap of block 0x%x to block 0x%x\\n", blk, dst);
					log_printf(0, "               this dump may have some bad data!\\n", blk, dst);
					dst = blk;
				}
			}
		}
'''
AX0 = [
    ('for', [(LOOP0, '''	for (blk = 0; blk < blocks; blk++) {
		src = raw + blk * 528 * ppb;
''')]),
]
JOIN = '''			dst = blk;
		}
%s		if (dst != blk) {
			if (blk >= blocks - 32)
				log_printf(1, "copying nanddump data from block 0x%%x to block 0x%%x for file extraction integrity\\n", blk, dst);
			else {
				log_printf(0, "***** WARNING: ignoring possible remap of block 0x%%x to block 0x%%x\\n", blk, dst);
				log_printf(0, "               this dump may have some bad data!\\n", blk, dst);
				dst = blk;
			}
		}
'''
AX1 = [
    ('else', []),
    ('else-nohot', [('rem: __attribute__((hot));\n', '')]),
    ('join', [(ARM, JOIN % '')]),
    ('join-hot', [(ARM, JOIN % 'rem: __attribute__((hot));\n')]),
]
AXES = [AX0, AX1]
