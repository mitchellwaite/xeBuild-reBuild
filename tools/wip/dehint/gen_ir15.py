"""parseDump: keep `dest < numBlocks` (its prediction lowers the log block's frequency; without it
blk is hoisted out of the loop), make it provable with a signed test on an unsigned counter."""
FOCUS = ['_parseDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt1.c'
LOOP = '''	for (n = 0; n < blocks; n++) {
		blk = n;
		src = raw + blk * 528 * ppb;
'''
AX0 = [
    ('cast', [(LOOP, '''	for (n = 0; (int)n < blocks; n++) {
		blk = n;
		src = raw + blk * 528 * ppb;
''')]),
    ('asg', [(LOOP, '''	for (n = 0; (blk = n) < blocks; n++) {
		src = raw + blk * 528 * ppb;
''')]),
    ('asg2', [(LOOP, '''	n = 0;
	while ((blk = n) < blocks) {
		n++;
		src = raw + blk * 528 * ppb;
''')]),
    ('cast2', [(LOOP, '''	for (n = 0; (int)n < blocks; n++) {
		blk = (int)n;
		src = raw + blk * 528 * ppb;
''')]),
]
AX1 = [('u1', [('''			if (blk >= blocks)
				__builtin_unreachable();
			if (blk < blocks) {
				log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
				if (!addRemapP(blk, blk, blk, -1, blocks))
					return 0;
			}
''', '''			log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
			if (!addRemapP(blk, blk, blk, -1, blocks))
				return 0;
''')])]
AX2 = [('', [('''		if (blk >= blocks)
			__builtin_unreachable();
		if (dst != blk &&''', '''		if (dst != blk &&''')])]
AX3 = [('bk', []), ('b', [('''			__asm__("");
			dst = blk;
''', '''			dst = blk;
''')])]
AX4 = [('ck', []), ('c', [('''	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));
''', '')])]
AX5 = [('pk', []), ('p', [('''			__asm__("" : "+r"(b2));
''', '')])]
AXES = [AX0, AX1, AX2, AX3, AX4, AX5]
