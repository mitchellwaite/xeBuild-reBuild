"""loadFlashFile, noinline gone: forms that are a little bigger at IPA time (size 45, limit: growth 39 must become 40+) and the same after VRP/ch.  `if (left > 0x4000) do ... while` first."""
FOCUS = ['_loadFlashFile', '_imgGetSecurityFiles']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
NI = 'int loadFlashFile(int i, uint32_t block) __attribute__((noinline));'
NI0 = 'int loadFlashFile(int i, uint32_t block);'
LF = '''	while (left > 0x4000) {
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
S = '''memcpy(xb.flashBuf[i] + done, xb.dump + off, 0x4000);
		left -= 0x4000;
		done += 0x4000;
		block = SWAP16(fs->map[block]) & 0x1fff;
		off = fsOffset + (block << 14);
'''
E = '''	if (left)
		memcpy(xb.flashBuf[i] + done, xb.dump + off, left);
	return verifyFlashFile(i);
'''
F = {
    'dw': 'if (left > 0x4000) {\n do {\n' + S + '} while (left > 0x4000);\n }\n' + E,
    'dw2': 'if (left > 0x4000) {\n do {\n' + S + '} while (left > 0x4000);\n if (left)\n memcpy(xb.flashBuf[i] + done, xb.dump + off, left);\n return verifyFlashFile(i);\n }\n' + E,
    'wa': 'while (left > 0x4000) {\n' + S + '}\n if (left > 0) {\n memcpy(xb.flashBuf[i] + done, xb.dump + off, left);\n }\n return verifyFlashFile(i);\n',
    'dbl': 'if (left) {\n while (left > 0x4000) {\n' + S + '}\n if (left)\n memcpy(xb.flashBuf[i] + done, xb.dump + off, left);\n }\n return verifyFlashFile(i);\n',
    'dbl2': 'if (left) {\n while (left > 0x4000) {\n' + S + '}\n memcpy(xb.flashBuf[i] + done, xb.dump + off, left);\n }\n return verifyFlashFile(i);\n',
    'el': 'if (left > 0x4000) {\n while (left > 0x4000) {\n' + S + '}\n }\n' + E,
    'lim': 'while (left) {\n uint32_t n = left > 0x4000 ? 0x4000 : left;\n memcpy(xb.flashBuf[i] + done, xb.dump + off, n);\n left -= n;\n done += n;\n block = SWAP16(fs->map[block]) & 0x1fff;\n off = fsOffset + (block << 14);\n }\n return verifyFlashFile(i);\n',
}
AXES = [[('', [(NI, NI0)])], [(k, [(LF, v)]) for k, v in F.items()]]
