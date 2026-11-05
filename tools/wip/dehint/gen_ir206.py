"""loadDump, no hot label: forms where ret takes notZeropair's value and is tested (gen_ir205's `r` is 6 loose: only `mov edi,1`'s constant missing) (attempt 14)."""
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
M = 'memcmp(zeropair, xb.dump + 16, 14)'
FORMS = {
 'a': 'ret = notZeropair(); if (!ret) ' + LOG + ' else ret = 1;',
 'b': 'ret = notZeropair(); if (ret) ret = 1; else ' + LOG,
 'b2': 'ret = notZeropair(); if (ret) ret = 1; else { ' + LOG + ' ret = 0; }',
 'c': 'ret = notZeropair(); if (!ret) { ' + LOG + ' ret = 0; } else ret = 1;',
 'd': 'ret = notZeropair() ? 1 : 0; if (!ret) ' + LOG,
 'e': 'ret = 1; if (!notZeropair()) { ' + LOG + ' ret = 0; }',
 'f': 'ret = 1; if (notZeropair() == 0) { ' + LOG + ' ret = 0; }',
 'g': 'ret = notZeropair(); if (ret) { ret = 1; } else { ' + LOG + ' }',
 'h': 'ret = !!notZeropair(); if (!ret) ' + LOG,
 'i': 'if (!(ret = notZeropair())) ' + LOG,
 'j': 'int nz = notZeropair(); ret = 1; if (!nz) { ' + LOG + ' ret = 0; }',
 'k': 'int nz = notZeropair(); ret = 0; if (nz) ret = 1; else ' + LOG,
 'l': 'ret = 0; if (notZeropair()) ret = 1; else ' + LOG,
 'm': 'ret = 0; if (!notZeropair()) ' + LOG + ' else ret = 1;',
 'n': 'ret = 1; if (!notZeropair()) ret = 0; if (!ret) ' + LOG,
 'o': 'ret = 0; if (notZeropair()) ret = 1; if (!ret) ' + LOG,
 'p': 'ret = notZeropair() != 0; if (ret == 0) ' + LOG,
 'q': 'ret = ' + M + '; if (ret) ret = 1; else ' + LOG,
 'q2': 'ret = ' + M + '; if (!ret) ' + LOG + ' else ret = 1;',
 'q3': 'ret = ' + M + ' ? 1 : 0; if (!ret) ' + LOG,
 'q4': 'ret = ' + M + ' != 0; if (!ret) ' + LOG,
 'q5': 'ret = 1; if (!' + M + ') { ' + LOG + ' ret = 0; }',
 'q6': 'ret = 0; if (' + M + ') ret = 1; if (!ret) ' + LOG,
}
F = [(k, [(COPY0, WO % v)]) for k, v in FORMS.items()]
RET = [
 ('ru', []),
 ('ri', [('	uint32_t ret;\n	uint32_t pages, rawSize;\n', '	int ret;\n	uint32_t pages, rawSize;\n')]),
]
AXES = [F, RET]
