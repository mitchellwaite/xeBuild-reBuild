"""parseDump without the dead test: the loop's return mass comes from addRemap's MAX REMAPS exit (3% in each inlined copy).  Forms of addRemap's end, to move it: entry must fall below 60 (irfq.py)."""
BASE = 'build/ir/a5/nod.c'
FOCUS = ['_parseDump', '_addRemap']
FOUND = '''	if (found)
		return 1;
'''
OLD = FOUND + '''	if (xb.numBad < 32) {
		if (dest != -1)
			log_printf(1, "block 0x%x was remapped to block 0x%x, entering remap instance %d\\n", block, dest, xb.numBad + 1);
		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad] = dest;
		xb.numBad++;
		return 1;
	}
	log_printf(1, "MAX REMAPS of 32 exceeded, remapping disabled and image rejected as faulty!\\n");
	return 0;
}
'''
ADD = '''		if (dest != -1)
			log_printf(1, "block 0x%x was remapped to block 0x%x, entering remap instance %d\\n", block, dest, xb.numBad + 1);
		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad] = dest;
		xb.numBad++;
'''
MAX = 'log_printf(1, "MAX REMAPS of 32 exceeded, remapping disabled and image rejected as faulty!\\n");\n'
AX = [
    ('k', []),
    ('ge', [(OLD, FOUND + '	if (xb.numBad >= 32) {\n' + MAX + '		return 0;\n	}\n' + ADD + '	return 1;\n}\n')]),
    ('else', [(OLD, FOUND + '	if (xb.numBad < 32) {\n' + ADD + '		return 1;\n	} else {\n' + MAX + '		return 0;\n	}\n}\n')]),
    ('elge', [(OLD, FOUND + '	if (xb.numBad >= 32) {\n' + MAX + '		return 0;\n	} else {\n' + ADD + '		return 1;\n	}\n}\n')]),
    ('nest', [(OLD, '	if (!found) {\n		if (xb.numBad < 32) {\n' + ADD + '			return 1;\n		}\n' + MAX + '		return 0;\n	}\n	return 1;\n}\n')]),
    ('nest2', [(OLD, '	if (!found) {\n		if (xb.numBad >= 32) {\n' + MAX + '			return 0;\n		}\n' + ADD + '	}\n	return 1;\n}\n')]),
    ('flag', [(OLD, '	if (!found) {\n		if (xb.numBad < 32) {\n' + ADD + '			found = 1;\n		} else\n' + MAX + '	}\n	return found;\n}\n')]),
    ('flag2', [(OLD, '	if (!found) {\n		if (xb.numBad >= 32) {\n' + MAX + '		} else {\n' + ADD + '			found = 1;\n		}\n	}\n	return found;\n}\n')]),
    ('eq32', [(OLD, FOUND + '	if (xb.numBad == 32) {\n' + MAX + '		return 0;\n	}\n' + ADD + '	return 1;\n}\n')]),
    ('ne32', [(OLD, FOUND + '	if (xb.numBad != 32) {\n' + ADD + '		return 1;\n	}\n' + MAX + '	return 0;\n}\n')]),
]
AXES = [AX]
