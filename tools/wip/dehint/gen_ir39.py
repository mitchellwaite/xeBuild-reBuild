"""checkBlock's pin_t: spellings of the MU test without the asm."""
FOCUS = ['_checkBlock']
BASE = 'tools/wip/dehint/drafts/image_read_attempt2.c'
OLD = '''				uint8_t m = b[524] & 0x3f;
				int t = m;

				/* opaque int copy: the <= 0x29 test stays an int
				   compare and isn't merged with the zero test */
				__asm__("" : "+d"(t));
				if (t <= 0x29 && m) {
'''
TAIL = '''					log_printf(0, "\\n\\n****************  WARNING  *************************\\n");
					log_printf(0, "  nanddump.bin has NAND memory unit data, make\\n");
					log_printf(0, "  sure you back up any important data off the\\n");
					log_printf(0, "  internal MU before flashing a new image!\\n");
					if (xb.bootFlags & 0x10000000) {
						log_printf(0, "\\n  xeBuild will attempt to keep this data, but\\n");
						log_printf(0, "  many things could cause it to be invalid/corrupt.\\n");
					}
					log_printf(0, "****************************************************\\n\\n");
					xb.muChecked = 1;
					xb.nandMu = 1;
				}
'''
H = {
    'and0': 'uint8_t m = b[524] & 0x3f;\n\nif (m <= 0x29 && m) {\n',
    'and1': 'uint8_t m = b[524] & 0x3f;\n\nif (m && m <= 0x29) {\n',
    'int': 'int m = b[524] & 0x3f;\n\nif (m <= 0x29 && m) {\n',
    'int2': 'int m = b[524] & 0x3f;\n\nif (m && m <= 0x29) {\n',
    'cross': 'uint8_t m = b[524];\n\nif ((m & 0x3f) <= 0x29 && (m & 0x3f)) {\n',
    'cross2': 'uint8_t m = b[524] & 0x3f;\nint t = m;\n\nif (t <= 0x29 && m) {\n',
    'cross3': 'uint8_t m = b[524] & 0x3f;\nint t = m;\n\nif (m && t <= 0x29) {\n',
    'cross4': 'int t = b[524] & 0x3f;\nuint8_t m = t;\n\nif (t <= 0x29 && m) {\n',
    'lt': 'uint8_t m = b[524] & 0x3f;\n\nif (m < 0x2a && m) {\n',
    'ne': 'uint8_t m = b[524] & 0x3f;\n\nif (m < 0x2a && m != 0) {\n',
}
NEST = {
    'n1': 'uint8_t m = b[524] & 0x3f;\n\nif (m <= 0x29) {\nif (m) {\n',
    'n2': 'uint8_t m = b[524] & 0x3f;\n\nif (m) {\nif (m <= 0x29) {\n',
    'n3': 'int m = b[524] & 0x3f;\n\nif (m <= 0x29) {\nif (m) {\n',
    'n4': 'int m = b[524] & 0x3f;\n\nif (m) {\nif (m <= 0x29) {\n',
    'n5': 'uint8_t m = b[524] & 0x3f;\nint t = m;\n\nif (t <= 0x29) {\nif (m) {\n',
    'n6': 'int t = b[524] & 0x3f;\nuint8_t m = t;\n\nif (t <= 0x29) {\nif (m) {\n',
    'n7': 'uint8_t m = b[524];\n\nif ((m & 0x3f) <= 0x29) {\nif (m & 0x3f) {\n',
    'n8': 'uint8_t m = b[524] & 0x3f;\n\nif (m < 0x2a) {\nif (m != 0) {\n',
}
V = [(k, [(OLD + TAIL, v + TAIL)]) for k, v in H.items()]
V += [(k, [(OLD + TAIL, v + TAIL + '}\n')]) for k, v in NEST.items()]
AXES = [V]
