"""remapBadBlocks: the loop guard of findFreeRemap's inlined scan, without the unreachable."""
FOCUS = ['_remapBadBlocks', '_findFreeRemap']
BASE = 'tools/wip/dehint/drafts/image_read_attempt1.c'
U = '''			if (!xb.numBad)	/* i < numBad: drops the inlined loop's guard */
				__builtin_unreachable();
'''
RD = '''void remapBadBlocks(int numBlocks)
{
	uint32_t i;
	int b;
'''
RL = '''	for (i = 0; i < xb.numBad; i++) {
		if (xb.badRemap[i] != -1)
			continue;
		if (xb.badBlocks[i] < numBlocks - 32) {
'''
FD = '''	int b, used;
	uint32_t i;

	for (b = numBlocks - 1;'''
FL = '''		used = 0;
		for (i = 0; i < xb.numBad; i++)
			if (xb.badRemap[i] == b || xb.badBlocks[i] == b) {
				used = 1;
				i = xb.numBad;
			}
		if (!used)
			return b;
'''
AX0 = [('', [(U, '')])]
AX1 = [('ru', []), ('ri', [(RD, RD.replace('uint32_t i', 'int i'))])]
AX2 = [('fu', []), ('fi', [(FD, FD.replace('uint32_t i', 'int i'))])]
AX3 = [('rl', []),
       ('rnest', [(RL, '''	for (i = 0; i < xb.numBad; i++) {
		if (xb.badRemap[i] == -1) {
		if (xb.badBlocks[i] < numBlocks - 32) {
'''), ('''			log_printf(1, "block 0x%x had no need of remap, it's in the wear area\\n", xb.badBlocks[i]);
			xb.badRemap[i] = -5;
		}
''', '''			log_printf(1, "block 0x%x had no need of remap, it's in the wear area\\n", xb.badBlocks[i]);
			xb.badRemap[i] = -5;
		}
		}
''')]),
       ]
AX4 = [('fl', []),
       ('fdo', [(FL, '''		used = 0;
		i = 0;
		do {
			if (xb.badRemap[i] == b || xb.badBlocks[i] == b)
				used = 1;
			i++;
		} while (!used && i < xb.numBad);
		if (!used)
			return b;
''')]),
       ('fnest', [(FL, '''		used = 0;
		for (i = 0; i < xb.numBad; i++) {
			if (xb.badRemap[i] == b) {
				used = 1;
				i = xb.numBad;
			} else if (xb.badBlocks[i] == b) {
				used = 1;
				i = xb.numBad;
			}
		}
		if (!used)
			return b;
''')]),
       ('fwh', [(FL, '''		used = 0;
		i = 0;
		while (i < xb.numBad) {
			if (xb.badRemap[i] == b || xb.badBlocks[i] == b) {
				used = 1;
				i = xb.numBad;
			}
			i++;
		}
		if (!used)
			return b;
''')]),
       ]
AXES = [AX0, AX1, AX2, AX3, AX4]
