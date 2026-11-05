"""attempt 4 base (signed loop, real addRemap, no parseDump hints): natural spellings that shift the free list so that blk's ch2 name lands low."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt4_base.c'
FOCUS = ['_parseDump']
A = [('', []),
     ('elif', [('''			dst = blk;
		}
		if (dst != blk) {
			if (blk >= blocks - 32)''', '''			dst = blk;
		} else if (dst != blk) {
			if (blk >= blocks - 32)''')])]
B = [('', []),
     ('cont', [('''				return 0;
			goto next;
''', '''				return 0;
			continue;
''')]),
     ]
C = [('', []),
     ('nest', [('''		if (dst != blk && !addRemap(dst, blk, blocks))
			return 0;
''', '''		if (dst != blk) {
			if (!addRemap(dst, blk, blocks))
				return 0;
		}
''')])]
D = [('', []),
     ('rri', [('''	int rr = xb.dumpPages % ppb;

	if (rr) {''', '''	if (xb.dumpPages % ppb) {''')])]
E = [('', []),
     ('ge', [('''	if (xb.numBad < 32) {
		if (dest != -1)
			log_printf(1, "block 0x%x was remapped to block 0x%x, entering remap instance %d\\n", block, dest, xb.numBad + 1);
		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad] = dest;
		xb.numBad++;
		return 1;
	}
	log_printf(1, "MAX REMAPS of 32 exceeded, remapping disabled and image rejected as faulty!\\n");
	return 0;
''', '''	if (xb.numBad >= 32) {
		log_printf(1, "MAX REMAPS of 32 exceeded, remapping disabled and image rejected as faulty!\\n");
		return 0;
	}
	if (dest != -1)
		log_printf(1, "block 0x%x was remapped to block 0x%x, entering remap instance %d\\n", block, dest, xb.numBad + 1);
	xb.badBlocks[xb.numBad] = block;
	xb.badRemap[xb.numBad] = dest;
	xb.numBad++;
	return 1;
''')])]
F = [('', []), ('ui', [('	uint32_t n;\n	int i;\n', '	uint32_t i;\n')]), ('rn', [('	uint32_t n;\n', '')])]
G = [('', []),
     ('dm1', [('if (!addRemap(blk, dst, blocks))', 'if (!addRemap(blk, -1, blocks))')])]
H = [('', []),
     ('src', [('''	uint8_t *src;

''', '''
'''), ('		src = raw + blk * 528 * ppb;\n', '		uint8_t *src = raw + blk * 528 * ppb;\n\n')])]
AXES = [A, B, C, D, E, F, G, H]
