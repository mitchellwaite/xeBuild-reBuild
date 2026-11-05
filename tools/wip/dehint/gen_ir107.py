"""loadFlashFile, noinline gone, more forms (gen_ir106: if + while isn't inlined, RA left): off computed where it's used, a helper for the sector's address, statement orders, guard kinds."""
FOCUS = ['_loadFlashFile', '_imgGetSecurityFiles']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
NI = 'int loadFlashFile(int i, uint32_t block) __attribute__((noinline));'
NI0 = 'int loadFlashFile(int i, uint32_t block);'
LF = '''	uint32_t off = fsOffset + (block << 14);
	uint32_t left = xb.flashSize[i];
	uint32_t done = 0;

	xb.flashBuf[i] = calloc(left, 1);
	while (left > 0x4000) {
		memcpy(xb.flashBuf[i] + done, xb.dump + off, 0x4000);
		left -= 0x4000;
		done += 0x4000;
		block = SWAP16(fs->map[block]) & 0x1fff;
		off = fsOffset + (block << 14);
	}
	if (left)
		memcpy(xb.flashBuf[i] + done, xb.dump + off, left);
	return verifyFlashFile(i);
'''
D = '''	uint32_t off;
	uint32_t left = xb.flashSize[i];
	uint32_t done = 0;

	xb.flashBuf[i] = calloc(left, 1);
'''
D1 = D.replace('	uint32_t off;\n', '')
OFF = 'off = fsOffset + (block << 14);\n'
NX = 'block = SWAP16(fs->map[block]) & 0x1fff;\n'
RV = 'return verifyFlashFile(i);\n'
M1 = 'memcpy(xb.flashBuf[i] + done, xb.dump + off, 0x4000);\n'
M2 = 'memcpy(xb.flashBuf[i] + done, xb.dump + off, left);\n'
M1d = 'memcpy(xb.flashBuf[i] + done, xb.dump + fsOffset + (block << 14), 0x4000);\n'
M2d = 'memcpy(xb.flashBuf[i] + done, xb.dump + fsOffset + (block << 14), left);\n'
M1e = 'memcpy(xb.flashBuf[i] + done, xb.dump + (fsOffset + (block << 14)), 0x4000);\n'
M2e = 'memcpy(xb.flashBuf[i] + done, xb.dump + (fsOffset + (block << 14)), left);\n'
A = 'left -= 0x4000;\n done += 0x4000;\n'
F = {
    'top': D + f'while (left > 0x4000) {{ {OFF} {M1} {A} {NX} }}\n if (left) {{ {OFF} {M2} }}\n {RV}',
    'top2': D + f'while (left > 0x4000) {{ {OFF} {M1} {A} {NX} }}\n {OFF} if (left) {{ {M2} }}\n {RV}',
    'd1': D1 + f'while (left > 0x4000) {{ {M1d} {A} {NX} }}\n if (left) {{ {M2d} }}\n {RV}',
    'e1': D1 + f'while (left > 0x4000) {{ {M1e} {A} {NX} }}\n if (left) {{ {M2e} }}\n {RV}',
    'ini': D + f'{OFF} while (left > 0x4000) {{ {M1} {A} {NX} {OFF} }}\n if (left) {{ {M2} }}\n {RV}',
    'ini2': D + f'{OFF} while (left > 0x4000) {{ {M1} {A} {NX} {OFF} }}\n if (left) {{ {OFF} {M2} }}\n {RV}',
}
D2 = '''	uint32_t off = fsOffset + (block << 14);
	uint32_t left = xb.flashSize[i];
	uint32_t done = 0;

	xb.flashBuf[i] = calloc(left, 1);
'''
L = f'while (left > 0x4000) {{ {M1} {A} {NX} {OFF} }}\n'
L2 = f'while (left > 0x4000) {{ {M1} {A} {NX} }}\n'
F = {
    'i3': D2 + L + f'if (left) {{ {OFF} {M2} }}\n {RV}',
    'i4': D2 + L + f'{OFF} if (left) {{ {M2} }}\n {RV}',
    'i5': D2 + L + f'if (left) {{ {M2d} }}\n {RV}',
    'i6': D2 + L + f'if (left) {{ {M2e} }}\n {RV}',
    'i7': D2 + f'while (left > 0x4000) {{ {M1} {A} {NX} off = fsOffset + (block << 14); }}\n if (left) {{ off = (block << 14) + fsOffset; {M2} }}\n {RV}',
    'i8': D2 + f'while (left > 0x4000) {{ {M1} done += 0x4000; left -= 0x4000; {NX} {OFF} }}\n if (left) {{ {OFF} {M2} }}\n {RV}',
    'i9': D2 + f'while (left > 0x4000) {{ {M1} {NX} {OFF} {A} }}\n if (left) {{ {OFF} {M2} }}\n {RV}',
    'i10': D2 + f'while (left > 0x4000) {{ {M1} {A} {NX} {OFF} }}\n if (left) {{ {M2} }}\n {RV}',
    'ini2': D + f'{OFF} while (left > 0x4000) {{ {M1} {A} {NX} {OFF} }}\n if (left) {{ {OFF} {M2} }}\n {RV}',
}
AXES = [[('', [(NI, NI0)])], [(k, [(LF, v)]) for k, v in F.items()]]
