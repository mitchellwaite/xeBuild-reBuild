"""the `ui` base: uncprop's reuse of the NOREMAP test's zero (test BYTE) and the entry frequency / summary's epilogue copy (threshold entry*100/1000 against the tail's freq 5)."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt4_base.c'
FOCUS = ['_parseDump']
I = [('ui', [('	uint32_t n;\n	int i;\n', '	uint32_t i;\n')])]
SUM = '''	if (xb.bootFlags & 0x40000000) {
		if (xb.numBad) {
			log_printf(1, "Discarding remap data as NOREMAP was specified!\\n");
			xb.numBad = 0;
		}
	} else if (xb.numBad) {
		remapBadBlocks(blocks);
		log_printf(1, "--remap summary--\\n");
		for (i = 0; i < xb.numBad; i++) {
			if (xb.badRemap[i] == -5)
				log_printf(1, "%d: source: 0x%04x dest: (NONE/BAD)\\n", i, xb.badBlocks[i]);
			else
				log_printf(1, "%d: source: 0x%04x dest: 0x%04x\\n", i, xb.badBlocks[i], xb.badRemap[i]);
		}
		log_printf(1, "-----------------\\n");
	}
	return 1;
'''
BODY = '''		remapBadBlocks(blocks);
		log_printf(1, "--remap summary--\\n");
		for (i = 0; i < xb.numBad; i++) {
			if (xb.badRemap[i] == -5)
				log_printf(1, "%d: source: 0x%04x dest: (NONE/BAD)\\n", i, xb.badBlocks[i]);
			else
				log_printf(1, "%d: source: 0x%04x dest: 0x%04x\\n", i, xb.badBlocks[i], xb.badRemap[i]);
		}
		log_printf(1, "-----------------\\n");
'''
DISC = '''		if (xb.numBad) {
			log_printf(1, "Discarding remap data as NOREMAP was specified!\\n");
			xb.numBad = 0;
		}
'''
T = {'cur': SUM}
for k, c in (('', 'xb.bootFlags & 0x40000000'), ('c', '(int)xb.bootFlags & 0x40000000'), ('c2', '(int)(xb.bootFlags & 0x40000000)'), ('s', '(xb.bootFlags >> 30) & 1'), ('v', '(xb.bootFlags & 0x40000000) != 0')):
    T['a' + k] = '	if (' + c + ') {\n' + DISC + '	} else if (xb.numBad) {\n' + BODY + '	}\n	return 1;\n'
    T['b' + k] = '	if (!(' + c + ')) {\n		if (xb.numBad) {\n' + BODY.replace('\t\t', '\t\t\t') + '		}\n	} else if (xb.numBad) {\n			log_printf(1, "Discarding remap data as NOREMAP was specified!\\n");\n			xb.numBad = 0;\n	}\n	return 1;\n'
    T['n' + k] = '	if (xb.numBad) {\n		if (' + c + ') {\n			log_printf(1, "Discarding remap data as NOREMAP was specified!\\n");\n			xb.numBad = 0;\n		} else {\n' + BODY.replace('\t\t', '\t\t\t') + '		}\n	}\n	return 1;\n'
    T['m' + k] = '	if (' + c + ') {\n' + DISC + '		return 1;\n	}\n	if (xb.numBad) {\n' + BODY + '	}\n	return 1;\n'
    T['r' + k] = '	if (' + c + ') {\n' + DISC + '	} else {\n		if (xb.numBad) {\n' + BODY.replace('\t\t', '\t\t\t') + '		}\n	}\n	return 1;\n'
AS = [(k, [(SUM, v)]) for k, v in T.items()]
AX = [('', []), ('ii', [('	uint32_t i;\n', '	int i;\n')])]
AXES = [I, AS, AX]
