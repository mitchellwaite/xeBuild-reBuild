"""detectController: the lba spellings, as checkBlock writes them, with pins removed."""
FOCUS = ['_detectController']
BASE = 'tools/wip/dehint/drafts/image_read_attempt1.c'
OLD = '''			int hi, lo;

			if (b[517] != 0xff || b[513] == 0xff)
				continue;
			hi = (b[514] & 0xf) * 256;
			lo = b[513];
			if (hi + lo == i) {
				i = n;
				log_printf(1, "\\tNAND dump uses big block controller\\n");
				xb.dumpBbController = 1;
				found = 1;
			} else {
				int lo2 = b[512];

				/* lo kept live past its add, so the sum takes hi's
				   register (ebp) */
				__asm__("" : : "a"(lo));
				if (lo2 + (b[513] & 0xf) * 256 == i) {
					__asm__("" : : "d"(lo2));
					i = n;
					log_printf(1, "\\tNAND dump uses small block controller\\n");
					xb.dumpBbController = 0;
					found = 1;
				}
			}
'''
BB = '''i = n;
				log_printf(1, "\\tNAND dump uses big block controller\\n");
				xb.dumpBbController = 1;
				found = 1;
'''
SB = '''i = n;
					log_printf(1, "\\tNAND dump uses small block controller\\n");
					xb.dumpBbController = 0;
					found = 1;
'''
T1 = {
    'hl': ('int hi, lo;', 'hi = (b[514] & 0xf) * 256;\nlo = b[513];\n', 'hi + lo == i'),
    'lh': ('int hi, lo;', 'lo = b[513];\nhi = (b[514] & 0xf) * 256;\n', 'hi + lo == i'),
    'lh2': ('int hi, lo;', 'lo = b[513];\nhi = (b[514] & 0xf) * 256;\n', 'lo + hi == i'),
    'hl2': ('int hi, lo;', 'hi = (b[514] & 0xf) * 256;\nlo = b[513];\n', 'lo + hi == i'),
    'e1': ('', '', 'b[513] + (b[514] & 0xf) * 256 == i'),
    'e2': ('', '', '(b[514] & 0xf) * 256 + b[513] == i'),
    'v1': ('int lba;', 'lba = b[513] + (b[514] & 0xf) * 256;\n', 'lba == i'),
    'v2': ('int lba;', 'lba = (b[514] & 0xf) * 256 + b[513];\n', 'lba == i'),
    'v3': ('int lba;', 'lba = b[513] + ((b[514] & 0xf) << 8);\n', 'lba == i'),
}
T2 = {
    'el': ('', 'b[512] + (b[513] & 0xf) * 256 == i'),
    'er': ('', '(b[513] & 0xf) * 256 + b[512] == i'),
    'lo2': ('int lo2 = b[512];\n', 'lo2 + (b[513] & 0xf) * 256 == i'),
    'lo2r': ('int lo2 = b[512];\n', '(b[513] & 0xf) * 256 + lo2 == i'),
    'hi2': ('int hi2 = (b[513] & 0xf) * 256;\n', 'hi2 + b[512] == i'),
    'lb': ('int lba0 = b[512] + (b[513] & 0xf) * 256;\n', 'lba0 == i'),
    'lbr': ('int lba0 = (b[513] & 0xf) * 256 + b[512];\n', 'lba0 == i'),
}
SH = {}
for k, (d, s, c) in T1.items():
    for l, (d2, c2) in T2.items():
        SH[k + '.' + l + '.else'] = f'''{d}

			if (b[517] != 0xff || b[513] == 0xff)
				continue;
			{s}if ({c}) {{
				{BB}}} else {{
				{d2}if ({c2}) {{
					{SB}}}
			}}
'''
AXES = [[(k, [(OLD, v)]) for k, v in SH.items()],
        [('', []), ('nopf', [('''		if (n > 1)
			__asm__("" : "+a"(found));
''', '')])]]
