"""base3: addRemap's conversion of block gets its name from the free list at PRE; reference: lower than the load's.  Natural forms of the function that shift the list."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt4_base3.c'
LOG1 = 'log_printf(1, "block 0x%x was remapped to block 0x%x at remap instance %d\\n", block, dest, i);\n'
L = '''	for (i = 0; i < xb.numBad; i++) {
		if (block == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {
			''' + LOG1 + '''			xb.badRemap[i] = dest;
			found = 1;
		}
	}
'''
FORMS = {
 '': L,
 'n3': '''	for (i = 0; i < xb.numBad; i++) {
		if (block == xb.badBlocks[i]) {
			if (xb.badRemap[i] == -1) {
				if (dest < numBlocks) {
					''' + LOG1 + '''					xb.badRemap[i] = dest;
					found = 1;
				}
			}
		}
	}
''',
 'n2': '''	for (i = 0; i < xb.numBad; i++) {
		if (block == xb.badBlocks[i] && xb.badRemap[i] == -1) {
			if (dest < numBlocks) {
				''' + LOG1 + '''				xb.badRemap[i] = dest;
				found = 1;
			}
		}
	}
''',
 'n1': '''	for (i = 0; i < xb.numBad; i++) {
		if (block == xb.badBlocks[i]) {
			if (xb.badRemap[i] == -1 && dest < numBlocks) {
				''' + LOG1 + '''				xb.badRemap[i] = dest;
				found = 1;
			}
		}
	}
''',
 'c': '''	for (i = 0; i < xb.numBad; i++) {
		if (block != xb.badBlocks[i] || xb.badRemap[i] != -1 || dest >= numBlocks)
			continue;
		''' + LOG1 + '''		xb.badRemap[i] = dest;
		found = 1;
	}
''',
 'w': '''	i = 0;
	while (i < xb.numBad) {
		if (block == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {
			''' + LOG1 + '''			xb.badRemap[i] = dest;
			found = 1;
		}
		i++;
	}
''',
 'u': L.replace('if (block == xb.badBlocks[i]', 'if ((uint32_t)block == xb.badBlocks[i]'),
 'r': L.replace('block == xb.badBlocks[i] && xb.badRemap[i] == -1', 'xb.badBlocks[i] == block && xb.badRemap[i] == -1'),
 'g': L.replace('dest < numBlocks', 'numBlocks > dest'),
}
A = [(k, [(L, v)]) for k, v in FORMS.items()]
B = [('', []),
     ('f0', [('	uint32_t i;\n	int found = 0;\n', '	uint32_t i;\n	uint32_t found = 0;\n')]),
     ('f1', [('	uint32_t i;\n	int found = 0;\n', '	int found = 0;\n	uint32_t i;\n')]),
     ('f2', [('	uint32_t i;\n	int found = 0;\n', '	uint32_t i, found = 0;\n')]),
     ('f3', [('	uint32_t i;\n	int found = 0;\n', '	uint32_t i = 0;\n	int found = 0;\n'), ('for (i = 0; i < xb.numBad; i++) {\n		if (block', 'for (; i < xb.numBad; i++) {\n		if (block')]) if False else ('', []),
     ]
ENT = 'log_printf(1, "block 0x%x was remapped to block 0x%x, entering remap instance %d\\n", block, dest, xb.numBad + 1);\n'
MAX = 'log_printf(1, "MAX REMAPS of 32 exceeded, remapping disabled and image rejected as faulty!\\n");\n'
RET = '''	if (found)
		return 1;
	if (xb.numBad < 32) {
		if (dest != -1)
			''' + ENT + '''		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad] = dest;
		xb.numBad++;
		return 1;
	}
	''' + MAX + '''	return 0;
'''
C = [('', []),
     ('nf2', [(RET, '''	if (!found) {
		if (xb.numBad < 32) {
			if (dest != -1)
				''' + ENT + '''			xb.badBlocks[xb.numBad] = block;
			xb.badRemap[xb.numBad] = dest;
			xb.numBad++;
		} else {
			''' + MAX + '''			return 0;
		}
	}
	return 1;
''')]),
     ('s', [('''		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad] = dest;
		xb.numBad++;
''', '''		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad++] = dest;
''')]),
     ('e', [(RET, '''	if (found)
		return 1;
	if (xb.numBad < 32) {
		if (dest != -1)
			''' + ENT + '''		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad] = dest;
		xb.numBad++;
		return 1;
	} else {
		''' + MAX + '''		return 0;
	}
''')]),
     ]
AXES = [A, B, C]
