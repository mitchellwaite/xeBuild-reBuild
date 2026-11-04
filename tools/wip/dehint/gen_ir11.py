"""parseDump: a signed loop counter.  VRP knows blocks >= 0 (uint / {32,256}), so `0 < blocks`
folds to `blocks != 0` (the reference's je), and blk < blocks is known in the body, which is what
the two __builtin_unreachable say."""
FOCUS = ['_parseDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt1.c'
LOOP = '''	for (n = 0; n < blocks; n++) {
		blk = n;
		src = raw + blk * 528 * ppb;
'''
AX0 = [('signed', [(LOOP, '''	for (blk = 0; blk < blocks; blk++) {
		src = raw + blk * 528 * ppb;
'''), ('''	uint32_t n;
	int i;
	uint8_t *src;
''', '''	int i;
	uint8_t *src;
''')])]
AXU1 = [('u1keep', []), ('u1', [('''			if (blk >= blocks)
				__builtin_unreachable();
			if (blk < blocks) {''', '''			if (blk < blocks) {''')])]
AXU2 = [('u2keep', []), ('u2', [('''		if (blk >= blocks)
			__builtin_unreachable();
		if (dst != blk &&''', '''		if (dst != blk &&''')])]
AXB = [('bkeep', []), ('b', [('''			__asm__("");
			dst = blk;
''', '''			dst = blk;
''')])]
AXC = [('ckeep', []), ('c', [('''	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));
''', '')])]
AXP = [('pkeep', []), ('p', [('''			__asm__("" : "+r"(b2));
''', '')])]
AXES = [AX0, AXU1, AXU2, AXB, AXC, AXP]
