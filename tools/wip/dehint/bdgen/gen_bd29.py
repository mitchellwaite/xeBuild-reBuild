# checkBl: per-arm crc errors (gen_bd28 per) with the size error's return value hidden from the local
# predictor by a helper, so it isn't 2%.  Needs size error >= 10%, default arm's share then falls under 10%.
REMOVE = ['cb5', 'lab_size', 'crc5', 'crc7', 'crc8', 'crc9', 'crc10', 'crc12', 'crc13']
FOCUS = ['_checkBl']
MSG = '''log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);'''
GOTO = 'if (crc != c)\n\t\t\tgoto bad;\n'
PER = 'if (crc != c) {\n\t\t\t' + MSG + '\n\t\t\treturn -2;\n\t\t}\n'
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
A = [('g', []), ('per', [(GOTO, PER)])]
T = [
    ('t0', []),
    ('help', [(SZ, 'toobig:\n\treturn blTooBig(blsize, size);\n'), (HEAD, HELP + HEAD)]),
    ('helpg', [(SZ, 'toobig:\n\treturn blTooBig(blsize, size);\n'), (HEAD, HELP + HEAD),
               ('	if (blsize > size)\n		goto toobig;\n', '	if (blsize > size)\n		return blTooBig(blsize, size);\n')]),
]
AXES = [A, T]
