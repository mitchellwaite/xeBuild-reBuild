"""base3: another invariant conversion above block's in the loop, so PRE's first insertion (name _40) is that one and block's gets _1 (below the load)."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt4_base3.c'
LOG1 = 'log_printf(1, "block 0x%x was remapped to block 0x%x at remap instance %d\\n", block, dest, i);\n'
L = '''	for (i = 0; i < xb.numBad; i++) {
		if (block == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {
			''' + LOG1 + '''			xb.badRemap[i] = dest;
			found = 1;
		}
	}
'''
F = {
 'd': '''	for (i = 0; i < xb.numBad; i++) {
		uint32_t d = dest;

		if (block == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {
			''' + LOG1 + '''			xb.badRemap[i] = d;
			found = 1;
		}
	}
''',
 'b': '''	for (i = 0; i < xb.numBad; i++) {
		uint32_t b = block;

		if (b == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {
			''' + LOG1 + '''			xb.badRemap[i] = dest;
			found = 1;
		}
	}
''',
 'bd': '''	for (i = 0; i < xb.numBad; i++) {
		uint32_t b = block;
		uint32_t d = dest;

		if (b == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {
			''' + LOG1 + '''			xb.badRemap[i] = d;
			found = 1;
		}
	}
''',
 'db': '''	for (i = 0; i < xb.numBad; i++) {
		uint32_t d = dest;
		uint32_t b = block;

		if (b == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {
			''' + LOG1 + '''			xb.badRemap[i] = d;
			found = 1;
		}
	}
''',
 'l': '''	for (i = 0; i < xb.numBad; i++) {
		uint32_t v = xb.badBlocks[i];

		if (block == v && xb.badRemap[i] == -1 && dest < numBlocks) {
			''' + LOG1 + '''			xb.badRemap[i] = dest;
			found = 1;
		}
	}
''',
 'lb': '''	for (i = 0; i < xb.numBad; i++) {
		uint32_t b = block;
		uint32_t v = xb.badBlocks[i];

		if (b == v && xb.badRemap[i] == -1 && dest < numBlocks) {
			''' + LOG1 + '''			xb.badRemap[i] = dest;
			found = 1;
		}
	}
''',
 'lt': '''	for (i = 0; i < xb.numBad; i++) {
		int ok = dest < numBlocks;

		if (block == xb.badBlocks[i] && xb.badRemap[i] == -1 && ok) {
			''' + LOG1 + '''			xb.badRemap[i] = dest;
			found = 1;
		}
	}
''',
 'lt2': '''	for (i = 0; i < xb.numBad; i++) {
		int ok = dest < numBlocks;

		if (block == xb.badBlocks[i]) {
			if (xb.badRemap[i] == -1 && ok) {
				''' + LOG1 + '''				xb.badRemap[i] = dest;
				found = 1;
			}
		}
	}
''',
}
AXES = [[('', [])] + [(k, [(L, v)]) for k, v in F.items()]]
