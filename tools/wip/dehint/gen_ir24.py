"""parseDump: start of attempt 2.  Signed for loop (u1, u2, bar_p, pin_cb, pin_b2 all gone), axes on
what's left: loop spelling, how src is computed, blk's declaration."""
FOCUS = ['_parseDump']
LOOP = '''	for (n = 0; n < blocks; n++) {
		blk = n;
		src = raw + blk * 528 * ppb;
'''
AX0 = [
    ('for', [(LOOP, '''	for (blk = 0; blk < blocks; blk++) {
		src = raw + blk * 528 * ppb;
''')]),
    ('forn', [(LOOP, '''	for (n = 0; (int)n < blocks; n++) {
		blk = n;
		src = raw + blk * 528 * ppb;
''')]),
]
AX1 = [('', [('''			if (blk >= blocks)
				__builtin_unreachable();
			if (blk < blocks) {
				log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
				if (!addRemapP(blk, blk, blk, -1, blocks))
					return 0;
			}
			__asm__("");
''', '''			log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
			if (!addRemapP(blk, blk, blk, -1, blocks))
				return 0;
''')])]
AX2 = [('', [('''		if (blk >= blocks)
			__builtin_unreachable();
		if (dst != blk &&''', '''		if (dst != blk &&''')])]
AX4 = [('', [('''	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));
''', '')])]
AX5 = [('', [('''			b2 = blk;
			__asm__("" : "+r"(b2));
			if (!addRemapP(b2, blk, 0, dst, blocks))
''', '''			if (!addRemapP(blk, blk, 0, dst, blocks))
''')])]
AXES = [AX0, AX1, AX2, AX4, AX5]
