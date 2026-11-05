"""loadDump: mmcbad and the != (size == 0) test gone: calling copyMmcImage (switch body from gen_ir141) or the copy written out with a switch.
s* have case 0 and default; x* a third edge VRP folds (notZeropair is 0 or 1), so even probabilities at profile_estimate."""
FOCUS = ['_copyMmcImage', '_loadDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt8.c'
CPY = '''uint32_t copyMmcImage(uint8_t *raw)
{
	xb.numBad = 0;
	memcpy(xb.dump, raw, xb.dumpSize);
	switch (notZeropair()) {
	case 0:
		log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");
		return 0;
	default:
		return 1;
	}
}
'''
USE = '''		if (xb.dumpMmc) {
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
'''
LOG = 'log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");\n'
HEAD = 'uint32_t copyMmcImage(uint8_t *raw)\n{\n xb.numBad = 0;\n memcpy(xb.dump, raw, xb.dumpSize);\n'
M = 'memcmp(zeropair, xb.dump + 16, 14)'
BODY = {
 's1': CPY,
 's2': HEAD + f'switch ({M}) {{ case 0: {LOG} return 0; default: return 1; }}\n}}\n',
 's3': HEAD + f'switch (notZeropair()) {{ case 0: {LOG} break; default: return 1; }} return 0;\n}}\n',
 's4': HEAD + f'switch (notZeropair()) {{ default: return 1; case 0: {LOG} return 0; }}\n}}\n',
 's5': HEAD + f'switch (notZeropair()) {{ case 1: return 1; default: {LOG} return 0; }}\n}}\n',
 's6': HEAD + f'switch (notZeropair()) {{ case 1: return 1; case 0: {LOG} }} return 0;\n}}\n',
 's7': HEAD + f'uint32_t r = 0; switch (notZeropair()) {{ case 0: {LOG} break; default: r = 1; }} return r;\n}}\n',
 's8': HEAD + f'uint32_t r; switch (notZeropair()) {{ case 0: {LOG} r = 0; break; default: r = 1; }} return r;\n}}\n',
 'x1': HEAD + f'switch (notZeropair()) {{ case 0: {LOG} return 0; case 1: return 1; default: return 0; }}\n}}\n',
 'x2': HEAD + f'switch (notZeropair()) {{ case 0: {LOG} return 0; case 1: return 1; default: return 2; }}\n}}\n',
 'x3': HEAD + f'switch (notZeropair()) {{ case 1: return 1; case 0: {LOG} return 0; default: return 0; }}\n}}\n',
 'x4': HEAD + f'switch (notZeropair()) {{ case 0: {LOG} return 0; case 1: return 1; }}\n return 0;\n}}\n',
 'x5': HEAD + f'switch (notZeropair()) {{ case 0: {LOG} return 0; case 1: return 1; }}\n return 2;\n}}\n',
 'x6': HEAD + f'uint32_t r = 2; switch (notZeropair()) {{ case 0: {LOG} r = 0; break; case 1: r = 1; break; }}\n return r;\n}}\n',
 'x7': HEAD + f'uint32_t r = 0; switch (notZeropair()) {{ case 0: {LOG} break; case 1: r = 1; break; }}\n return r;\n}}\n',
 'x9': HEAD + f'switch (notZeropair()) {{ case 1: return 1; default: return 0; case 0: {LOG} return 0; }}\n}}\n',
}
UFORMS = {
 'if': '		if (xb.dumpMmc) ret = copyMmcImage(raw);\n		else\n',
 'nif': '		if (!xb.dumpMmc) ret = parseDump(raw); else ret = copyMmcImage(raw);\n		if (0)\n',
}
AXES = [[(k, [(CPY, v)]) for k, v in BODY.items()], [(k, [(USE, v)]) for k, v in UFORMS.items()]]
