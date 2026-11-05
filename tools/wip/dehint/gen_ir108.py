"""fsGetFile, pin_v gone: IRA pops by thread freq, and the rival of the return value is off (r106), not name: thread 582 with the loop's border allocnos.  Forms of off in the copy loop."""
FOCUS = ['_fsGetFile']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
PV = '''	/* code-free hint: fsValid (reused for return 1) in esi, name in edi */
	__asm__("" : : "S"(v));
'''
OLD = '''	off = fsOffset + (block << 14);
	p = calloc(len, 1);
	left = len;
	done = 0;
	while (left > 0x4000) {
		memcpy(p + done, xb.dump + off, 0x4000);
		left -= 0x4000;
		done += 0x4000;
		block = SWAP16(fs->map[block]) & 0x1fff;
		off = fsOffset + (block << 14);
	}
	if (left)
		memcpy(p + done, xb.dump + off, left);
'''
OFF = 'off = fsOffset + (block << 14);\n'
M1 = 'memcpy(p + done, xb.dump + off, 0x4000);\n'
M2 = 'memcpy(p + done, xb.dump + off, left);\n'
M1d = 'memcpy(p + done, xb.dump + fsOffset + (block << 14), 0x4000);\n'
M2d = 'memcpy(p + done, xb.dump + fsOffset + (block << 14), left);\n'
A = 'left -= 0x4000;\n done += 0x4000;\n'
NX = 'block = SWAP16(fs->map[block]) & 0x1fff;\n'
H = 'p = calloc(len, 1);\n left = len;\n done = 0;\n'
F = {
    'r': OFF + H + f'while (left > 0x4000) {{ {M1} {A} {NX} {OFF} }}\n if (left) {{ {OFF} {M2} }}\n',
    'r2': OFF + H + f'while (left > 0x4000) {{ {M1} {A} {NX} {OFF} }}\n {OFF} if (left) {{ {M2} }}\n',
    't': H + f'while (left > 0x4000) {{ {OFF} {M1} {A} {NX} }}\n if (left) {{ {OFF} {M2} }}\n',
    't2': H + f'while (left > 0x4000) {{ {OFF} {M1} {A} {NX} }}\n {OFF} if (left) {{ {M2} }}\n',
    'd': H + f'while (left > 0x4000) {{ {M1d} {A} {NX} }}\n if (left) {{ {M2d} }}\n',
    'l': OFF + H + f'while (left > 0x4000) {{ {M1} {A} {NX} {OFF} }}\n if (left) {{ {M2d} }}\n',
    'o': OLD,
}
AXES = [[('', [(PV, '')])], [(k, [(OLD, v)]) for k, v in F.items()]]
