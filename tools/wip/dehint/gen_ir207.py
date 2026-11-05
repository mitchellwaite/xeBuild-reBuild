"""loadDump, no hot label: gen_ir206's `n` (ret = 1; if (!nz) ret = 0; if (!ret) log) has only two alignments wrong.  The success block's alignment wants
(1 - P(test2)) * 105 + P(test1) * 104 > 91, so test2 at P(success) <= 62.  Forms of both tests, written out or the real copyMmcImage (attempt 14)."""
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
SW = '''	switch (notZeropair()) {
	case 0:
		log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");
		return 0;
	default:
		return 1;
	}
'''
T1 = {
 'a': 'ret = 1; if (!notZeropair()) ret = 0;',
 'b': 'ret = 0; if (notZeropair()) ret = 1;',
 'c': 'if (notZeropair()) ret = 1; else ret = 0;',
 'd': 'if (!notZeropair()) ret = 0; else ret = 1;',
}
T2 = {
 'z': 'if (!ret) ' + LOG,
 'ne1': 'if (ret != 1) ' + LOG,
 'gt': 'if (ret > 0) ; else ' + LOG,
 'le': 'if ((int)ret <= 0) ' + LOG,
 'lt1': 'if (ret < 1) ' + LOG,
 'ne1e': 'if (ret == 1) ; else ' + LOG,
}
RT = [('ru', []), ('ri', [('	uint32_t ret;\n	uint32_t pages, rawSize;\n', '	int ret;\n	uint32_t pages, rawSize;\n')])]
F = []
for a, t1 in T1.items():
    for b, t2 in T2.items():
        F.append(('w.%s.%s' % (a, b), [(COPY0, WO % (t1 + ' ' + t2))]))
        # the real function, ret local
        F.append(('c.%s.%s' % (a, b), [(COPY0, '		if (xb.dumpMmc)\n			ret = copyMmcImage(raw);\n		else\n			ret = parseDump(raw);\n'),
                                       (SW, '	uint32_t ret;\n	' + t1 + ' ' + t2 + '	return ret;\n')]))
AXES = [F, RT]
