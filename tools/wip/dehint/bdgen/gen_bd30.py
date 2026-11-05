# checkBl with the size-error helper (toobig 20.7%): bad is 14.4%, it needs under 10%.  Each arm's crc failure
# goes to `bad` (keeps c's PHI) or has its own log and return -2 (its return prediction lowers it).
REMOVE = ['cb5', 'lab_size', 'crc5', 'crc7', 'crc8', 'crc9', 'crc10', 'crc12', 'crc13']
FOCUS = ['_checkBl']
MSG = '''log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);'''
GOTO = '		if (crc != c)\n			goto bad;\n'
PER = '		if (crc != c) {\n			' + MSG + '\n			return -2;\n		}\n'
SZ = '''toobig:
	log_printf(0, "\\n\\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\\n", blsize, size);
	return -3;
'''
HEAD = '''__attribute__((optimize("no-early-inlining")))
int checkBl('''
HELP = '''/* the size error, for checkBl */
static int blTooBig(uint32_t blsize, uint32_t size)
{
	log_printf(0, "\\n\\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\\n", blsize, size);
	return -3;
}

'''
ARMS = {
    5: "	case 17:\n		if (bl[1] != 'B')\n			goto magic;\n		memset(bl + 0x10, 0, 0x30);\n		c = crc32(bl, blsize);\n",
    7: "	case 18:\n		if (bl[1] != 'D')\n			goto magic;\n		memset(bl + 0x10, 0, 0x10);\n		c = crc32(bl, blsize);\n",
    8: "	case 19:\n		if (bl[1] != 'E')\n			goto magic;\n		memset(bl + 0x10, 0, 0x10);\n		c = crc32(bl, blsize);\n",
    9: "	case 20:\n		if (bl[1] != 'F')\n			goto magic;\n		memset(bl + 0x20, 0, 0x210);\n		c = crc32(bl, blsize);\n",
    10: "	case 21:\n		if (bl[1] != 'G')\n			goto magic;\n		memset(bl + 0x10, 0, 0x10);\n		c = crc32(bl, blsize);\n",
    12: "		if (bl[1] != 'C')\n			goto magic;\n		memset(bl + 0x10, 0, 0x10);\n		if (crc == 0xffffffff)\n			break;\n		c = crc32(bl, blsize);\n",
    13: "	case 13:\n		if (bl[1] != 'D')\n			goto magic;\n		memset(bl + 0x10, 0, 0x10);\n		if (crc == 0xffffffff)\n			break;\n		c = crc32(bl, blsize);\n",
    14: "		raiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));\n		if (crc == 0xffffffff)\n			break;\n		c = crc32(bl, blsize);\n",
}
AXES = [[('', [(SZ, 'toobig:\n\treturn blTooBig(blsize, size);\n'), (HEAD, HELP + HEAD)])]]
for k, v in ARMS.items():
    AXES.append([('', []), ('p%d' % k, [(v + GOTO, v + PER)])])
