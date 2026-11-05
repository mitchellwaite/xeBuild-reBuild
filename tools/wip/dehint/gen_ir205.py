"""loadDump + copyMmcImage + notZeropair, no hot label: types of ret, of the callees' returns, real copy called or written out, nested forms (attempt 14).
Same idea as detectController's `int found`: every hint off at once and sweep types."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
FOCUS = ['_loadDump', '_copyMmcImage', '_parseDump']
LOG = 'log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");\n'
COPY0 = '''		/* copyMmcImage's body, written out: calling it (it would inline) leaves
		   only the log block's place, since its switch is predicted 29% for
		   the log.  The test must be predicted 50-52.6%
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
WO = '''		if (xb.dumpMmc) {
			xb.numBad = 0;
			memcpy(xb.dump, raw, xb.dumpSize);
			%s
		} else
			ret = parseDump(raw);
'''
F = [
 ('ne', [(COPY0, WO % ('if (notZeropair() != (size == 0)) ret = 1; else { ' + LOG + ' ret = 0; }'))]),
 ('pl', [(COPY0, WO % ('if (notZeropair()) ret = 1; else { ' + LOG + ' ret = 0; }'))]),
 ('lg', [(COPY0, WO % ('if (!notZeropair()) { ' + LOG + ' ret = 0; } else ret = 1;'))]),
 ('r', [(COPY0, WO % ('ret = notZeropair(); if (!ret) ' + LOG))]),
 ('r2', [(COPY0, WO % ('ret = notZeropair(); if (ret <= 0) ' + LOG))]),
 ('r3', [(COPY0, WO % ('ret = 1; if (!notZeropair()) { ' + LOG + ' ret = 0; }'))]),
 ('s', [(COPY0, WO % ('switch (notZeropair()) { case 0: ' + LOG + ' ret = 0; break; default: ret = 1; }'))]),
 ('c', [(COPY0, '		if (xb.dumpMmc)\n			ret = copyMmcImage(raw);\n		else\n			ret = parseDump(raw);\n')]),
 ('c3', [(COPY0, '		ret = xb.dumpMmc ? copyMmcImage(raw) : parseDump(raw);\n')]),
]
RET = [
 ('ru', []),
 ('ri', [('	uint32_t ret;\n	uint32_t pages, rawSize;\n', '	int ret;\n	uint32_t pages, rawSize;\n')]),
 ('rl', [('	uint32_t ret;\n	uint32_t pages, rawSize;\n', '	unsigned long ret;\n	uint32_t pages, rawSize;\n')]),
]
NZ = [
 ('ni', []),
 ('nu', [('int notZeropair(void);', 'uint32_t notZeropair(void);'), ('int notZeropair(void)\n', 'uint32_t notZeropair(void)\n')]),
 ('nl', [('int notZeropair(void);', 'unsigned long notZeropair(void);'), ('int notZeropair(void)\n', 'unsigned long notZeropair(void)\n')]),
]
SW = '''	switch (notZeropair()) {
	case 0:
		log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");
		return 0;
	default:
		return 1;
	}
'''
CP = [
 ('cu', []),
 ('ci', [('uint32_t copyMmcImage(uint8_t *raw);', 'int copyMmcImage(uint8_t *raw);'), ('uint32_t copyMmcImage(uint8_t *raw)\n', 'int copyMmcImage(uint8_t *raw)\n')]),
 ('cl', [('uint32_t copyMmcImage(uint8_t *raw);', 'unsigned long copyMmcImage(uint8_t *raw);'), ('uint32_t copyMmcImage(uint8_t *raw)\n', 'unsigned long copyMmcImage(uint8_t *raw)\n')]),
 ('cui', [(SW, '	if (notZeropair())\n		return 1;\n	' + LOG + '	return 0;\n')]),
 ('cii', [('uint32_t copyMmcImage(uint8_t *raw);', 'int copyMmcImage(uint8_t *raw);'), ('uint32_t copyMmcImage(uint8_t *raw)\n', 'int copyMmcImage(uint8_t *raw)\n'), (SW, '	if (notZeropair())\n		return 1;\n	' + LOG + '	return 0;\n')]),
 ('cli', [('uint32_t copyMmcImage(uint8_t *raw);', 'unsigned long copyMmcImage(uint8_t *raw);'), ('uint32_t copyMmcImage(uint8_t *raw)\n', 'unsigned long copyMmcImage(uint8_t *raw)\n'), (SW, '	if (notZeropair())\n		return 1;\n	' + LOG + '	return 0;\n')]),
]
AXES = [F, RET, NZ, CP]
