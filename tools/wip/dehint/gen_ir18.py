"""loadFlashFile: growth 39, limit 40 (max-inline-insns-auto).  One more gimple statement at IPA time
that later passes fold keeps it out of imgGetSecurityFiles with no attribute."""
FOCUS = None
BASE = 'tools/wip/dehint/drafts/image_read_attempt1.c'
NO = [('int loadFlashFile(int i, uint32_t block) __attribute__((noinline));', 'int loadFlashFile(int i, uint32_t block);')]
LF = '''		xb.flashBuf[i] = calloc(left, 1);
	while (left > 0x4000) {
		memcpy(xb.flashBuf[i] + done, xb.dump + off, 0x4000);
		left -= 0x4000;
		done += 0x4000;
		block = SWAP16(fs->map[block]) & 0x1fff;
		off = fsOffset + (block << 14);
	}
'''
ST = '''	while (left > 0x4000) {
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
def body(sw):
    return ST.replace('block = SWAP16(fs->map[block]) & 0x1fff;', sw)
AX = [
    ('base', []),
    ('s_two', [(ST, body('block = SWAP16(fs->map[block]);\n\t\tblock &= 0x1fff;'))]),
    ('s_tmp', [(ST, body('{\n\t\t\tuint16_t next = fs->map[block];\n\t\t\tblock = SWAP16(next) & 0x1fff;\n\t\t}'))]),
    ('s_tmp32', [(ST, body('{\n\t\t\tuint32_t next = fs->map[block];\n\t\t\tblock = SWAP16(next) & 0x1fff;\n\t\t}'))]),
    ('s_iw', [(ST, body('block = SWAP16_IMAGE_WRITE(fs->map[block]) & 0x1fff;'))]),
    ('s_keys', [(ST, body('block = SWAP16_KEYS(fs->map[block]) & 0x1fff;'))]),
    ('s_build', [(ST, body('block = SWAP16_BUILD(fs->map[block]) & 0x1fff;'))]),
    ('s_rot', [(ST, body('block = ROT16(fs->map[block]) & 0x1fff;'))]),
    ('s_hi', [(ST, body('block = (SWAP16(fs->map[block]) & 0xffff) & 0x1fff;'))]),
    ('s_cast', [(ST, body('block = (uint16_t)SWAP16(fs->map[block]) & 0x1fff;'))]),
    ('r_ret', [(ST, ST.replace('return verifyFlashFile(i);', '{\n\t\tint ret = verifyFlashFile(i);\n\t\treturn ret;\n\t}'))]),
    ('p_buf', [(ST, ST.replace('memcpy(xb.flashBuf[i] + done, xb.dump + off, 0x4000);', 'memcpy(&xb.flashBuf[i][done], &xb.dump[off], 0x4000);'))]),
]
AXES = [[('', NO)], AX]
