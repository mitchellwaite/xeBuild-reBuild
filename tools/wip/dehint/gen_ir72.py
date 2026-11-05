"""base2: entry frequency against natural forms of addRemap (need entry 58-59)."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt4_base2.c'
FOCUS = ['_parseDump']
LOG1 = 'log_printf(1, "block 0x%x was remapped to block 0x%x at remap instance %d\\n", block, dest, i);\n'
L = '''	for (i = 0; i < xb.numBad; i++) {
		if (block == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {
			''' + LOG1 + '''			xb.badRemap[i] = dest;
			found = 1;
		}
	}
'''
NEST = '''	for (i = 0; i < xb.numBad; i++) {
		if (block == xb.badBlocks[i]) {
			if (xb.badRemap[i] == -1) {
				if (dest < numBlocks) {
					''' + LOG1 + '''					xb.badRemap[i] = dest;
					found = 1;
				}
			}
		}
	}
'''
NEST2 = '''	for (i = 0; i < xb.numBad; i++) {
		if (block == xb.badBlocks[i] && xb.badRemap[i] == -1) {
			if (dest < numBlocks) {
				''' + LOG1 + '''				xb.badRemap[i] = dest;
				found = 1;
			}
		}
	}
'''
A = [('', []), ('nest', [(L, NEST)]), ('nest2', [(L, NEST2)])]
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
B = [('', []),
     ('ge', [(RET, '''	if (found)
		return 1;
	if (xb.numBad >= 32) {
		''' + MAX + '''		return 0;
	}
	if (dest != -1)
		''' + ENT + '''	xb.badBlocks[xb.numBad] = block;
	xb.badRemap[xb.numBad] = dest;
	xb.numBad++;
	return 1;
''')]),
     ('nf', [(RET, '''	if (!found) {
		if (xb.numBad >= 32) {
			''' + MAX + '''			return 0;
		}
		if (dest != -1)
			''' + ENT + '''		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad] = dest;
		xb.numBad++;
	}
	return 1;
''')]),
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
     ('nf3', [(RET, '''	if (!found) {
		if (xb.numBad >= 32) {
			''' + MAX + '''			return 0;
		} else {
			if (dest != -1)
				''' + ENT + '''			xb.badBlocks[xb.numBad] = block;
			xb.badRemap[xb.numBad] = dest;
			xb.numBad++;
		}
	}
	return 1;
''')]),
     ]
AXES = [A, B]
