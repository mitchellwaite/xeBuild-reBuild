"""base3: standalone addRemap, PRE inserts the conversion of block as _40 and the next one as _1: one pop more or one dead name fewer before it gives the low name.  Forms that move the free list."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt4_base3.c'
LOG1 = 'log_printf(1, "block 0x%x was remapped to block 0x%x at remap instance %d\\n", block, dest, i);'
ENT = 'log_printf(1, "block 0x%x was remapped to block 0x%x, entering remap instance %d\\n", block, dest, xb.numBad + 1);'
A = [('', []),
     ('l1', [(LOG1, LOG1.replace('", block, dest', '", (uint32_t)block, dest'))]),
     ('l1d', [(LOG1, LOG1.replace('block, dest, i', 'block, (uint32_t)dest, i'))]),
     ]
B = [('', []),
     ('l2', [(ENT, ENT.replace('", block, dest', '", (uint32_t)block, dest'))]),
     ('l2d', [(ENT, ENT.replace('block, dest, xb', 'block, (uint32_t)dest, xb'))]),
     ]
ST = '''		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad] = dest;
		xb.numBad++;
'''
C = [('', []),
     ('s1', [(ST, '''		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad++] = dest;
''')]),
     ('s2', [(ST, '''		xb.badBlocks[xb.numBad] = (uint32_t)block;
		xb.badRemap[xb.numBad] = (uint32_t)dest;
		xb.numBad++;
''')]),
     ('s3', [(ST, '''		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad] = dest;
		xb.numBad += 1;
''')]),
     ('s4', [(ST, '''		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad] = dest;
		xb.numBad = xb.numBad + 1;
''')]),
     ]
CMP = 'if (block == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {'
D = [('', []),
     ('c1', [(CMP, 'if (block == xb.badBlocks[i] && xb.badRemap[i] == (uint32_t)-1 && dest < numBlocks) {')]),
     ('c2', [(CMP, 'if (block == xb.badBlocks[i] && (int)xb.badRemap[i] == -1 && dest < numBlocks) {')]),
     ('c3', [(CMP, 'if (block == xb.badBlocks[i] && xb.badRemap[i] == 0xffffffff && dest < numBlocks) {')]),
     ]
E = [('', []),
     ('fu', [('	uint32_t i;\n	int found = 0;\n', '	uint32_t i;\n	uint32_t found = 0;\n')]),
     ('f1', [('	uint32_t i;\n	int found = 0;\n', '	int found = 0;\n	uint32_t i;\n')]),
     ('dne', [('		if (dest != -1)\n			log_printf(1, "block 0x%x was remapped to block 0x%x, entering', '		if (dest + 1)\n			log_printf(1, "block 0x%x was remapped to block 0x%x, entering')]),
     ]
AXES = [A, B, C, D, E]
