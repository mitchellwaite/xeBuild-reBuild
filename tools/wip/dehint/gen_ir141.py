"""copyMmcImage, attribute gone, loadDump's written-out copy kept.  ce1's IF-CASE-2 stops if ELSE sets a register the test reads, or if ELSE has two predecessors, or SUCC(ELSE) doesn't postdominate THEN with P <= 50: forms where one of those holds."""
FOCUS = ['_copyMmcImage']
OLD = '''__attribute__((optimize("no-if-conversion"))) uint32_t copyMmcImage(uint8_t *raw)
{
	xb.numBad = 0;
	memcpy(xb.dump, raw, xb.dumpSize);
	if (notZeropair())
		return 1;
	log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");
	return 0;
}
'''
HD = 'uint32_t copyMmcImage(uint8_t *raw)\n{\n xb.numBad = 0;\n memcpy(xb.dump, raw, xb.dumpSize);\n'
LOG = 'log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");\n'
M = 'memcmp(zeropair, xb.dump + 16, 14)'
F = {
 'base': f'if (notZeropair()) return 1; {LOG} return 0;',
 'r1': f'uint32_t r = notZeropair(); if (r) r = 1; else {{ {LOG} r = 0; }} return r;',
 'r2': f'uint32_t r = notZeropair(); if (!r) {LOG} return r;',
 'r3': f'uint32_t r = {M}; if (r) r = 1; else {{ {LOG} r = 0; }} return r;',
 'r4': f'uint32_t r = {M}; if (r) r = 1; else {LOG} return r;',
 'r5': f'int r = {M}; if (r) r = 1; else {{ {LOG} }} return r;',
 'r6': f'int r = {M}; if (!r) {{ {LOG} return 0; }} return 1;',
 'r7': f'int r = {M}; if (!r) {LOG} return r != 0;',
 'r8': f'int r = {M}; if (r == 0) {LOG} return !!r;',
 'r9': f'int r = {M} != 0; if (!r) {LOG} return r;',
 's1': f'switch (notZeropair()) {{ case 0: {LOG} return 0; default: return 1; }}',
 's2': f'switch ({M}) {{ case 0: {LOG} return 0; default: return 1; }}',
 's3': f'switch ({M}) {{ case 0: {LOG} break; default: return 1; }} return 0;',
 't1': f'uint32_t ret = 0; if (notZeropair()) ret = 1; else {LOG} return ret;',
 't2': f'uint32_t ret = 1; if (!notZeropair()) {{ {LOG} ret = 0; }} return ret;',
 't3': f'uint32_t ret; if ({M}) ret = 1; else {{ {LOG} ret = 0; }} return ret;',
 't4': f'uint32_t ret = 1; if (!{M}) {{ {LOG} ret = 0; }} return ret;',
 't5': f'uint32_t ret = 0; if ({M}) ret = 1; else {LOG} return ret;',
 'g1': f'if (notZeropair()) goto ok; {LOG} return 0; ok: return 1;',
 'g2': f'if (!notZeropair()) goto bad; return 1; bad: {LOG} return 0;',
 'g3': f'if ({M} == 0) goto bad; return 1; bad: {LOG} return 0;',
 'c1': f'return notZeropair() ? 1 : (log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n"), 0);',
 'd1': f'if (notZeropair()) return 1; else {LOG} return 0;',
 'e1': f'if (!notZeropair()) {{ {LOG} return 0; }} return 1;',
 'f1': f'if ({M}) return 1; {LOG} return 0;',
 'f2': f'if (!{M}) {{ {LOG} return 0; }} return 1;',
 'f3': f'if ({M} == 0) {{ {LOG} return 0; }} else return 1;',
}
AX = [(k, [(OLD, HD + v + '\n}\n')]) for k, v in F.items()]
AXES = [AX]
