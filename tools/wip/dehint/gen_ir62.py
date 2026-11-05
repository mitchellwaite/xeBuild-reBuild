"""copyMmcImage: no attribute, loadDump calls it instead of a written out copy with a hot label (opt_mmc + lab_mmc).  Body and return types, how loadDump uses it, notZeropair's spelling."""
FOCUS = ['_copyMmcImage', '_loadDump', '_parseDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt3.c'
ATTR = '''/* ce1 would hoist ret = 1 above the branch (edge predicted 61%) */
__attribute__((optimize("no-if-conversion"))) uint32_t copyMmcImage(uint8_t *raw)
{
	xb.numBad = 0;
	memcpy(xb.dump, raw, xb.dumpSize);
	if (notZeropair())
		return 1;
	log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");
	return 0;
}
'''
USE = '''		/* copyMmcImage's body, written out: its optimize attribute keeps it
		   from being inlined here.  The test must be predicted 50-52.6%
		   (ce1 hoists ret = 1 only above 50%, the mmc trace takes the log
		   block only within 10% of even): call 71% x hot label 15% x opcode
		   nonequal 72% (the != against size == 0, folded by VRP) = 52.6% */
		if (xb.dumpMmc) {
			xb.numBad = 0;
			memcpy(xb.dump, raw, xb.dumpSize);
			if (notZeropair() != (size == 0))
				ret = 1;
			else {
mmcbad: __attribute__((hot));
				log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");
				ret = 0;
			}
		} else
			ret = parseDump(raw);
'''
LOG = 'log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");\n'
HEAD = 'uint32_t copyMmcImage(uint8_t *raw)\n{\n	xb.numBad = 0;\n	memcpy(xb.dump, raw, xb.dumpSize);\n'
B = {
    'k': HEAD + '	if (notZeropair())\n		return 1;\n	' + LOG + '	return 0;\n}\n',
    'n': HEAD + '	if (!notZeropair()) {\n		' + LOG + '		return 0;\n	}\n	return 1;\n}\n',
    'r': HEAD + '	if (notZeropair())\n		ret = 1;\n	else {\n		' + LOG + '		ret = 0;\n	}\n	return ret;\n}\n',
    'r2': HEAD + '	if (!notZeropair()) {\n		' + LOG + '		ret = 0;\n	} else\n		ret = 1;\n	return ret;\n}\n',
    'r3': HEAD + '	ret = 1;\n	if (!notZeropair()) {\n		' + LOG + '		ret = 0;\n	}\n	return ret;\n}\n',
    'r4': HEAD + '	ret = notZeropair();\n	if (!ret)\n		' + LOG + '	return ret;\n}\n',
}
for k in list(B):
    if 'ret' in B[k]:
        B[k] = B[k].replace('{\n	xb.numBad', '{\n	uint32_t ret;\n\n	xb.numBad', 1)
U = {
    'if': '		if (xb.dumpMmc)\n			ret = copyMmcImage(raw);\n		else\n			ret = parseDump(raw);\n',
    'q': '		ret = xb.dumpMmc ? copyMmcImage(raw) : parseDump(raw);\n',
    'nif': '		if (!xb.dumpMmc)\n			ret = parseDump(raw);\n		else\n			ret = copyMmcImage(raw);\n',
}
T = {'u32': [], 'ul': [('uint32_t copyMmcImage(uint8_t *raw)', 'unsigned long copyMmcImage(uint8_t *raw)')]}
AXB = [(k, [(ATTR, v)]) for k, v in B.items()]
AXU = [(k, [(USE, v)]) for k, v in U.items()]
AXZ = [('', []),
       ('zb', [('int notZeropair(void)\n{\n	return memcmp(zeropair, xb.dump + 16, 14) != 0;\n}', 'int notZeropair(void)\n{\n	if (memcmp(zeropair, xb.dump + 16, 14))\n		return 1;\n	return 0;\n}')]),
       ]
AXES = [AXB, AXU, AXZ]
