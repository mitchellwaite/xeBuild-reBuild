"""checkBl after blMagic: the crc expects as a helper call on each arm (PRED_CALL under no-early-inlining), size error by helper
or label.  bad < 1000, size in [1000, 2000), magic >= 1000."""
import re
CRC = '''		if (__builtin_expect(crc != c, 0))
			goto bad;
'''
MSG = 'log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);'
SZLOG = '	log_printf(0, "\\n\\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\\n", blsize, size);\n'
HEAD = '__attribute__((optimize("no-early-inlining")))\nint checkBl('
BADH = 'static int blBadCrc(uint32_t c, uint32_t crc)\n{\n	' + MSG + '\n	return -2;\n}\n\n'
BADV = 'static void blBadCrc(uint32_t c, uint32_t crc)\n{\n	' + MSG + '\n}\n\n'
ARMS = [
    ('e', []),
    ('h', [(CRC, '		if (crc != c)\n			return blBadCrc(c, crc);\n'), (HEAD, BADH + HEAD)]),
    ('v', [(CRC, '		if (crc != c) {\n			blBadCrc(c, crc);\n			return -2;\n		}\n'), (HEAD, BADV + HEAD)]),
    ('g', [(CRC, '		if (crc != c)\n			goto bad;\n')]),
]
BAD14 = [
    ('', []),
    ('b14', [('		if (crc != c)\n			goto bad;\n		break;\n	default:\n		c = 0;\n		goto bad;\n	}\n	return 0;\nbad:\n	' + MSG + '\n	return -2;\n',
              '		if (crc != c)\n			return blBadCrc(c, crc);\n		break;\n	default:\n		return blBadCrc(0, crc);\n	}\n	return 0;\n')]),
]
SZ = 'toobig: __attribute__((hot));\n' + SZLOG + '	return -3;\n'
SH = 'static int blTooBig(uint32_t blsize, uint32_t size)\n{\n' + SZLOG + '	return -3;\n}\n\n'
SIZE = [
    ('hot', []),
    ('plain', [(SZ, 'toobig:\n' + SZLOG + '	return -3;\n')]),
    ('help', [(SZ, 'toobig:\n	return blTooBig(blsize, size);\n'), (HEAD, SH + HEAD)]),
    ('help2', [(SZ, ''), ('	if (blsize > size)\n		goto toobig;\n', '	if (blsize > size)\n		return blTooBig(blsize, size);\n'), (HEAD, SH + HEAD)]),
]
AXES = [ARMS, SIZE]
FOCUS = ['_checkBl']
