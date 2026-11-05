"""loadDump's mmcbad at P(log) 51.2: ce1's IF-CASE-1 has no probability test (only cost) if the `ret = 1` block is T's fallthrough: split_edge_bb_loc puts it after T when the target's previous block has an edge to it, so test `if (ret)` with the success arm first."""
FOCUS = ['_copyMmcImage', '_loadDump']
BASE = 'src/image_read.c'
USE = '''			if (notZeropair() != (size == 0))
				ret = 1;
			else {
mmcbad: __attribute__((hot));
				log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");
				ret = 0;
			}
'''
LOG = 'log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");\n'
T = 'notZeropair() != (size != 0)'
F = {
 'ne': f'if ({T}) {{ {LOG} ret = 0; }} else ret = 1;\n',
 'ee': f'if (notZeropair() == (size != 0)) ret = 1; else {{ {LOG} ret = 0; }}\n',
 'pl': f'if (notZeropair()) ret = 1; else {{ {LOG} ret = 0; }}\n',
 'sw': f'switch (notZeropair()) {{ case 0: {LOG} ret = 0; break; default: ret = 1; }}\n',
}
TAIL_OLD = '''		if (!ret)
			buildCleanup();
		else {
'''
BODY_END = '''			getNonces();
		}
'''
TAILS = {
 't0': [(TAIL_OLD, TAIL_OLD)],
 't1': [(TAIL_OLD, '		if (ret) {\n'), (BODY_END, '			getNonces();\n		} else\n			buildCleanup();\n')],
 't2': [(TAIL_OLD, '		if (ret != 0) {\n'), (BODY_END, '			getNonces();\n		} else {\n			buildCleanup();\n		}\n')],
}
AX = []
for k, v in F.items():
    for tk, tv in TAILS.items():
        AX.append((k + '.' + tk, [(USE, v)] + tv))
AXES = [AX]
