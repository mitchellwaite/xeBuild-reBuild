"""loadDump's mmcbad: no hot label.  Log on the != side of a compare VRP folds, so opcode nonequal (72%) favours the log against call 29%: P(log) about 51%."""
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
F = {
 'ne': f'if (notZeropair() != (size != 0)) {{ {LOG} ret = 0; }} else ret = 1;\n',
 'eq': f'if (notZeropair() == (size != 0)) ret = 1; else {{ {LOG} ret = 0; }}\n',
 'ne2': f'if ((size != 0) != notZeropair()) {{ {LOG} ret = 0; }} else ret = 1;\n',
 'nv': f'{{ int nz = notZeropair(); if (nz != (size != 0)) {{ {LOG} ret = 0; }} else ret = 1; }}\n',
 'nr': f'ret = 1; if (notZeropair() != (size != 0)) {{ {LOG} ret = 0; }}\n',
 'n1': f'if (notZeropair() != 1) {{ {LOG} ret = 0; }} else ret = 1;\n',
 'e1': f'if (notZeropair() == 1) ret = 1; else {{ {LOG} ret = 0; }}\n',
 'ng': f'if (notZeropair() != (size > 0)) {{ {LOG} ret = 0; }} else ret = 1;\n',
 'plain': f'if (notZeropair()) ret = 1; else {{ {LOG} ret = 0; }}\n',
}
AXES = [[(k, [(USE, v)]) for k, v in F.items()]]
