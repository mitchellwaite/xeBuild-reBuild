"""checkBl: crc compared by a helper (no NONEQUAL prediction under no-early-inlining), failure's log written in the arm (a log helper
called 7 times isn't inlined in the cold arms)."""
CRC = '''		if (__builtin_expect(crc != c, 0))
			goto bad;
'''
MSG = 'log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);'
HEAD = '__attribute__((optimize("no-early-inlining")))\nint checkBl('
SAME = 'static int crcSame(uint32_t c, uint32_t crc)\n{\n	return c == crc;\n}\n\n'
DIFF = 'static int crcDiffers(uint32_t c, uint32_t crc)\n{\n	return crc != c;\n}\n\n'
ARMS = [
    ('same', [(CRC, '		if (!crcSame(c, crc)) {\n			' + MSG + '\n			return -2;\n		}\n'), (HEAD, SAME + HEAD)]),
    ('diff', [(CRC, '		if (crcDiffers(c, crc)) {\n			' + MSG + '\n			return -2;\n		}\n'), (HEAD, DIFF + HEAD)]),
    ('nofn', [(CRC, '		if (crc != c) {\n			' + MSG + '\n			return -2;\n		}\n')]),
]
SZ = 'toobig: __attribute__((hot));\n'
SIZE = [('hot', []), ('plain', [(SZ, 'toobig:\n')])]
PIN = [('', []), ('nopin', [('	__asm__("" : : "D"(type));\n', '')]), ('nom', [('	__asm__("" :: "a"(m));\n', '')])]
AXES = [ARMS, SIZE, PIN]
FOCUS = ['_checkBl']
