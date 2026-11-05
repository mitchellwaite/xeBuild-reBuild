"""loadFlashFile / fsGetFile copy loops as the Linux build shows them (`size - done > 0x4000` each time round, no `left` counter); noinline gone?  pin_v gone?"""
FOCUS = ['_loadFlashFile', '_imgGetSecurityFiles', '_fsGetFile']
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
BODY = '''	uint32_t off = fsOffset + (block << 14);
	uint32_t size = xb.flashSize[i];
	uint32_t done = 0;
	uint32_t left;

	xb.flashBuf[i] = calloc(size, 1);
	%s
	if (left)
		memcpy(xb.flashBuf[i] + done, xb.dump + off, left);
	return verifyFlashFile(i);
'''
STEP = '''memcpy(xb.flashBuf[i] + done, xb.dump + off, 0x4000);
		done += 0x4000;
		block = SWAP16(fs->map[block]) & 0x1fff;
		off = fsOffset + (block << 14);
'''
LOOPS = {
    'w': 'while (size - done > 0x4000) {\n' + STEP + '}\n left = size - done;\n',
    'l': 'left = size;\n while (left > 0x4000) {\n' + STEP + 'left = size - done;\n }\n',
    'l2': 'left = size - done;\n while (left > 0x4000) {\n' + STEP + 'left = size - done;\n }\n',
    'f': 'for (left = size; left > 0x4000; left = size - done) {\n' + STEP + '}\n',
    'g': 'for (left = size; left > 0x4000; left -= 0x4000) {\n' + STEP + '}\n',
}
AX1 = [(k, [(LF, BODY % v)]) for k, v in LOOPS.items()] + [('o', [])]
AXES = [[('ni0', [(NI, NI0)]), ('nik', [])], AX1]
