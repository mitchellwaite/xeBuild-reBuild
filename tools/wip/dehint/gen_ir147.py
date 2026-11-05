"""loadDump calls copyMmcImage (switch body): P(log) must be within 10% of even for the layout.  Hot label kept in the switch's case 0, or a block before the log at profile time (test VRP folds), or written out with a switch and the hot label."""
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
BODY = {
 'hot': HEAD + f'switch (notZeropair()) {{ case 0: mmcbad: __attribute__((hot)); {LOG} return 0; default: return 1; }}\n}}\n',
 'r': HEAD + f'int ok = notZeropair(); switch (ok) {{ case 0: if (!ok) {LOG} return ok; default: return 1; }}\n}}\n',
 'rw': HEAD + f'switch (notZeropair()) {{ case 0: if (raw) {LOG} return 0; default: return 1; }}\n}}\n',
 'rx': HEAD + f'int ok = notZeropair(); switch (ok) {{ case 0: if (ok == 0) {{ {LOG} }} break; default: return 1; }} return 0;\n}}\n',
 'lp': HEAD + f'int ok = notZeropair(); if (!ok) {{ switch (ok) {{ case 0: {LOG} }} }} return ok;\n}}\n',
 'lq': HEAD + f'int ok = notZeropair(); switch (ok) {{ default: return 1; case 0: break; }} {LOG} return 0;\n}}\n',
}
UFORMS = {
 'if': '		if (xb.dumpMmc) ret = copyMmcImage(raw);\n		else\n',
}
AXES = [[(k, [(CPY, v)]) for k, v in BODY.items()], [(k, [(USE, v)]) for k, v in UFORMS.items()]]
