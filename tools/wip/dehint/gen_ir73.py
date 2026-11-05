"""base2: an arm's test nested over a test VRP folds later: its probability reaches the rebuild and the guard goes away.  irfqp: -3 and -4 arms want 12-13%, -1 13%, -2 22-27%, site 3 52-53%.
`&&` of two cheap compares gimplifies to `a & b`, no opcode prediction: nested only."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt4_base2.c'
FOCUS = ['_parseDump']
AX = []
TESTS = {'ge0': 'blk >= 0', 'lt': 'blk < blocks', 'gtm': 'blk > -1', 'ne': 'blk != blocks'}
ARMS = {
 '-3': '''		if (dst == -3) {
			log_printf(0, "***** WARNING: nanddump.bin has a bad LBA at block 0x%x (raw offset 0x%x), block LBA ignored\\n", blk, src - raw);
			continue;
		}
''',
 '-6': '''		if (dst == -6) {
			log_printf(0, "***** WARNING: nanddump.bin has a mixed controller LBA at block 0x%x (raw offset 0x%x), block ignored\\n", blk, src - raw);
			log_printf(0, "               this is likely caused by previously using jaspersb on a jasper type console!\\n", blk, src - raw);
			continue;
		}
''',
 '-4': '''		if (dst == -4) {
			log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
			if (!addRemap(blk, -1, blocks))
				return 0;
			dst = blk;
		}
''',
 '-1': '''		if (dst == -1) {
			log_printf(1, "bad block at 0x%x (raw offset 0x%x), block ignored\\n", blk, src - raw);
			if (!addRemap(blk, dst, blocks))
				return 0;
			goto next;
		}
''',
}
for a, text in ARMS.items():
    for k, c in TESTS.items():
        lines = text.split('\n')
        inner = '\n'.join('\t' + l for l in lines[1:-2])
        AX.append(('n%s.%s' % (a, k), [(text, lines[0] + '\n\t\t\tif (' + c + ') {\n' + inner + '\n\t\t\t}\n\t\t}\n')]))
AXES = [AX]
