"""checkBl: per-arm blBadCrc merges to 1157 (crossjump adds the arms to bad); it must stay under 1000.  Arms need about a third of
their probability: no NONEQUAL prediction on the test (crc compared by a helper, seen as a call under no-early-inlining)."""
CRC = '''		if (__builtin_expect(crc != c, 0))
			goto bad;
'''
MSG = 'log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);'
HEAD = '__attribute__((optimize("no-early-inlining")))\nint checkBl('
BADV = 'static void blBadCrc(uint32_t c, uint32_t crc)\n{\n	' + MSG + '\n}\n\n'
SAME = 'static int crcSame(uint32_t c, uint32_t crc)\n{\n	return c == crc;\n}\n\n'
DIFF = 'static int crcDiffers(uint32_t c, uint32_t crc)\n{\n	return crc != c;\n}\n\n'
CHK = 'static int blCrcOk(uint32_t c, uint32_t crc)\n{\n	if (crc != c) {\n		' + MSG + '\n		return 0;\n	}\n	return 1;\n}\n\n'
CHK2 = 'static int blCrcOk(uint32_t c, uint32_t crc)\n{\n	if (crc == c)\n		return 1;\n	' + MSG + '\n	return 0;\n}\n\n'
CHKB = 'static int blCrcBad(uint32_t c, uint32_t crc)\n{\n	if (crc != c) {\n		' + MSG + '\n		return 1;\n	}\n	return 0;\n}\n\n'
CHKN = 'static int blCrcCheck(uint32_t c, uint32_t crc)\n{\n	if (crc != c) {\n		' + MSG + '\n		return -2;\n	}\n	return 0;\n}\n\n'
ARMS = [
    ('e', []),
    ('same-v', [(CRC, '		if (!crcSame(c, crc)) {\n			blBadCrc(c, crc);\n			return -2;\n		}\n'), (HEAD, BADV + SAME + HEAD)]),
    ('same-g', [(CRC, '		if (!crcSame(c, crc))\n			goto bad;\n'), (HEAD, SAME + HEAD)]),
    ('diff-v', [(CRC, '		if (crcDiffers(c, crc)) {\n			blBadCrc(c, crc);\n			return -2;\n		}\n'), (HEAD, BADV + DIFF + HEAD)]),
    ('diff-g', [(CRC, '		if (crcDiffers(c, crc))\n			goto bad;\n'), (HEAD, DIFF + HEAD)]),
    ('ok', [(CRC, '		if (!blCrcOk(c, crc))\n			return -2;\n'), (HEAD, CHK + HEAD)]),
    ('ok2', [(CRC, '		if (!blCrcOk(c, crc))\n			return -2;\n'), (HEAD, CHK2 + HEAD)]),
    ('badf', [(CRC, '		if (blCrcBad(c, crc))\n			return -2;\n'), (HEAD, CHKB + HEAD)]),
    ('chk', [(CRC, '		if (blCrcCheck(c, crc))\n			return -2;\n'), (HEAD, CHKN + HEAD)]),
    ('chkr', [(CRC, '		r = blCrcCheck(c, crc);\n		if (r)\n			return r;\n'), (HEAD, CHKN + HEAD), ('	uint32_t blsize, c;\n	int m;\n', '	uint32_t blsize, c;\n	int m, r;\n')]),
]
SZ = 'toobig: __attribute__((hot));\n'
SIZE = [('hot', []), ('plain', [(SZ, 'toobig:\n')])]
AXES = [ARMS, SIZE]
FOCUS = ['_checkBl']
