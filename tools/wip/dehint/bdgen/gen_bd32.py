# checkBl: all arms but 14 with their own crc error (bad 884, fine).  The size error is 2071 with the helper and needs
# to be under 2000 (round 3): other ways into it.  Base: gen_bd31's hg+all.
BASE = 'build/bd/gen_bd31_best.c'
FOCUS = ['_checkBl']
TEST = '	if (blsize > size)\n		goto toobig;\n'
TAIL = 'toobig:\n\treturn blTooBig(blsize, size);\n'
SZLOG = '''log_printf(0, "\\n\\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\\n", blsize, size);'''
H = '''static int blTooBig(uint32_t blsize, uint32_t size)
{
	''' + SZLOG + '''
	return -3;
}
'''
AXES = [[
    ('base', []),
    ('ternary', [('int m, dead;', 'int m, dead, r;'), (TEST, '	r = blsize > size ? blTooBig(blsize, size) : 0;\n	if (r)\n		return r;\n'), (TAIL, '')]),
    ('rvar', [('int m, dead;', 'int m, dead, r = 0;'), (TEST, '	if (blsize > size)\n		r = blTooBig(blsize, size);\n	if (r)\n		return r;\n'), (TAIL, '')]),
    ('rlate', [('int m, dead;', 'int m, dead, r = -3;'), (TAIL, 'toobig:\n\t' + SZLOG + '\n\treturn r;\n'), (H, 'static int blTooBig(void);\n')]),
    ('twolog', [(H, H.replace('	return -3;', '	return -3;')), (TAIL, 'toobig:\n\tif (blTooBig(blsize, size))\n\t\treturn -3;\n\treturn 0;\n')]),
]]
