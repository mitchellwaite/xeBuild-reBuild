# checkBl: size error in [1000, 2000) (round 3, epilogue copy); bad under 1000: per-arm crc errors except a few.
# gen_bd30 had the size error at 2071, in round 2.
REMOVE = ['cb5', 'lab_size', 'crc5', 'crc7', 'crc8', 'crc9', 'crc10', 'crc12', 'crc13']
FOCUS = ['_checkBl']
MSG = '''log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);'''
GOTO = '		if (crc != c)\n			goto bad;\n'
PER = '		if (crc != c) {\n			' + MSG + '\n			return -2;\n		}\n'
SZLOG = '''	log_printf(0, "\\n\\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\\n", blsize, size);
'''
SZ = 'toobig:\n' + SZLOG + '	return -3;\n'
HEAD = '''__attribute__((optimize("no-early-inlining")))
int checkBl('''
HELP = '''/* the size error, for checkBl */
static int blTooBig(uint32_t blsize, uint32_t size)
{
''' + SZLOG + '''	return -3;
}

'''
TEST = '	if (blsize > size)\n		goto toobig;\n'
BADTAIL = '''	return -2;
toobig:
	return blTooBig(blsize, size);
'''
SIZE = [
    ('hg', [(SZ, 'toobig:\n\treturn blTooBig(blsize, size);\n'), (HEAD, HELP + HEAD)]),
    ('hl', [(SZ, 'toobig:\n\t{\n\t\tint r = blTooBig(blsize, size);\n\n\t\treturn r;\n\t}\n'), (HEAD, HELP + HEAD)]),
    ('hn', [(SZ, 'toobig:\n\treturn blTooBig(blsize, size);\n'), (HEAD, HELP + HEAD), (TEST, '	if (blsize <= size) {\n'),
            ('	return -2;\ntoobig:\n	return blTooBig(blsize, size);\n', '	return -2;\n	}\n	return blTooBig(blsize, size);\n')]),
    ('hu', [(SZ, 'toobig:\n\treturn blTooBig(blsize, size);\n'), (HEAD, HELP.replace('static int', 'static uint32_t') + HEAD)]),
    ('ho', [(SZ, 'toobig:\n\treturn blTooBig(blsize, size);\n'), (HEAD, HELP + HEAD), (TEST, '	if (size < blsize)\n		goto toobig;\n')]),
]
ARMS = {
    5: "	case 17:\n		if (bl[1] != 'B')\n			goto magic;\n		memset(bl + 0x10, 0, 0x30);\n		c = crc32(bl, blsize);\n",
    7: "	case 18:\n		if (bl[1] != 'D')\n			goto magic;\n		memset(bl + 0x10, 0, 0x10);\n		c = crc32(bl, blsize);\n",
    8: "	case 19:\n		if (bl[1] != 'E')\n			goto magic;\n		memset(bl + 0x10, 0, 0x10);\n		c = crc32(bl, blsize);\n",
    9: "	case 20:\n		if (bl[1] != 'F')\n			goto magic;\n		memset(bl + 0x20, 0, 0x210);\n		c = crc32(bl, blsize);\n",
    10: "	case 21:\n		if (bl[1] != 'G')\n			goto magic;\n		memset(bl + 0x10, 0, 0x10);\n		c = crc32(bl, blsize);\n",
    12: "		if (bl[1] != 'C')\n			goto magic;\n		memset(bl + 0x10, 0, 0x10);\n		if (crc == 0xffffffff)\n			break;\n		c = crc32(bl, blsize);\n",
    13: "	case 13:\n		if (bl[1] != 'D')\n			goto magic;\n		memset(bl + 0x10, 0, 0x10);\n		if (crc == 0xffffffff)\n			break;\n		c = crc32(bl, blsize);\n",
}
ALL = [(v + GOTO, v + PER) for v in ARMS.values()]
PERS = [('g', []), ('all', ALL)]
for skip in ARMS:
    PERS.append(('allbut%d' % skip, [(ARMS[k] + GOTO, ARMS[k] + PER) for k in ARMS if k != skip]))
AXES = [SIZE, PERS]
