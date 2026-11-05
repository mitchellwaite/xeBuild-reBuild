"""checkBl: blCrcCheck per arm merges to 1083; bad must be under 1000.  Forms of the helper, type 14 through it too, and hand-merged
cases (5 and 7's table targets split would need duplicates: not here)."""
CRC = '''		if (__builtin_expect(crc != c, 0))
			goto bad;
'''
C14 = '''		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		break;
	default:
'''
MSG = 'log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);'
HEAD = '__attribute__((optimize("no-early-inlining")))\nint checkBl('
H = {
    'a': 'static int blCrcCheck(uint32_t c, uint32_t crc)\n{\n	if (crc != c) {\n		' + MSG + '\n		return -2;\n	}\n	return 0;\n}\n\n',
    'b': 'static int blCrcCheck(uint32_t c, uint32_t crc)\n{\n	if (crc == c)\n		return 0;\n	' + MSG + '\n	return -2;\n}\n\n',
    'c': 'static int blCrcCheck(uint32_t c, uint32_t crc)\n{\n	int r = 0;\n\n	if (crc != c) {\n		' + MSG + '\n		r = -2;\n	}\n	return r;\n}\n\n',
    'd': 'static int blCrcCheck(uint32_t crc, uint32_t c)\n{\n	if (c != crc) {\n		log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);\n		return 1;\n	}\n	return 0;\n}\n\n',
    'e': 'static int blCrcCheck(uint8_t *bl, uint32_t blsize, uint32_t crc)\n{\n	uint32_t c = crc32(bl, blsize);\n\n	if (crc != c) {\n		' + MSG + '\n		return -2;\n	}\n	return 0;\n}\n\n',
}
CALL = {
    'a': '		if (blCrcCheck(c, crc))\n			return -2;\n',
    'b': '		if (blCrcCheck(c, crc) != 0)\n			return -2;\n',
    'lt': '		if (blCrcCheck(c, crc) < 0)\n			return -2;\n',
}
A = []
for k, h in H.items():
    for ck, cv in CALL.items():
        if k == 'd':
            cv = cv.replace('blCrcCheck(c, crc)', 'blCrcCheck(crc, c)')
        if k == 'e':
            continue
        A.append((k + '-' + ck, [(CRC, cv), (HEAD, h + HEAD)]))
T14 = [('', []), ('t14', [(C14, '		c = crc32(bl, blsize);\n		if (blCrcCheck(c, crc))\n			return -2;\n		break;\n	default:\n')])]
AXES = [A, T14]
FOCUS = ['_checkBl']
