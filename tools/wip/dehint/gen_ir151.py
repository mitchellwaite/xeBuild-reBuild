"""loadDump's mmcbad: P(success) has to get from 48.8 (call + nonequal on the log's side) to 50-52.  Early return in the log arm (54%?), loop guard, etc."""
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
 'er': f'if ({T}) {{ {LOG} buildCleanup(); free(raw); return 0; }} ret = 1;\n',
 'er2': f'if ({T}) {{ {LOG} buildCleanup(); free(raw); return 0; }} else ret = 1;\n',
 'gt': f'if ({T}) {{ {LOG} goto fail; }} else ret = 1;\n',
 'gt2': f'if ({T}) {{ {LOG} ret = 0; goto fail; }} ret = 1;\n',
}
TAIL_OLD = '''		if (!ret)
			buildCleanup();
		else {
'''
TAILS = {
 't0': TAIL_OLD,
 't1': '''		if (!ret) {
fail:
			buildCleanup();
			ret = 0;
		} else {
''',
}
AX = []
for k, v in F.items():
    for tk, tv in TAILS.items():
        if ('gt' in k) != (tk == 't1'):
            continue
        AX.append((k + '.' + tk, [(USE, v), (TAIL_OLD, tv)]))
AXES = [AX]
