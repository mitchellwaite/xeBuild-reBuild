"""checkBl: whole-function shapes.  .rdata order is crc, size, magic, so the size error's text
comes after the crc one's"""
REMOVE = ['lit_chk', 'lab_size', 'cb5', 'crc5', 'crc7', 'crc8', 'crc9', 'crc10', 'crc12', 'crc13']
FOCUS = ['_checkBl']
SZ = 'log_printf(0, "\\n\\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\\n", blsize, size);'
BAD = 'log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);'
MAG = 'log_printf(0, "\\n\\n***** ERROR: BL magic check %c%c for type %d failed!\\n", bl[0], bl[1], type);'
H = '''	if (blsize > size) {
		''' + SZ + '''
		return -3;
	}
	m = bl[0];
	__asm__("" :: "a"(m));
	if ((m & 0x43) != 0x43)
		goto magic;
	switch (type) {
'''
T = '''	return 0;
bad:
	''' + BAD + '''
	return -2;
magic:
	''' + MAG + '''
	return -1;
}
'''
PM = '	__asm__("" :: "a"(m));\n'


def S(pin, label, head, tail):
    p = PM if pin else ''
    return (label + ('' if pin else '-m'), [(H, head.replace('@P', p)), (T, tail)])


shapes = []
for pin in (1, 0):
    shapes += [
        S(pin, 'orig', '''	if (blsize > size) {
		''' + SZ + '''
		return -3;
	}
	m = bl[0];
@P	if ((m & 0x43) != 0x43)
		goto magic;
	switch (type) {
''', T),
        S(pin, 'le_goto', '''	if (blsize <= size) {
	m = bl[0];
@P	if ((m & 0x43) != 0x43)
		goto magic;
	switch (type) {
''', '''	return 0;
bad:
	''' + BAD + '''
	return -2;
	}
	''' + SZ + '''
	return -3;
magic:
	''' + MAG + '''
	return -1;
}
'''),
        S(pin, 'le_else', '''	if (blsize <= size) {
	m = bl[0];
@P	if ((m & 0x43) != 0x43)
		goto magic;
	switch (type) {
''', '''	return 0;
bad:
	''' + BAD + '''
	return -2;
	} else {
	''' + SZ + '''
	return -3;
	}
magic:
	''' + MAG + '''
	return -1;
}
'''),
        S(pin, 'gt_goto', '''	if (blsize > size)
		goto toobig;
	m = bl[0];
@P	if ((m & 0x43) != 0x43)
		goto magic;
	switch (type) {
''', '''	return 0;
bad:
	''' + BAD + '''
	return -2;
toobig:
	''' + SZ + '''
	return -3;
magic:
	''' + MAG + '''
	return -1;
}
'''),
        S(pin, 'nest2', '''	if (blsize <= size) {
	m = bl[0];
@P	if ((m & 0x43) == 0x43) {
	switch (type) {
''', '''	return 0;
bad:
	''' + BAD + '''
	return -2;
	}
magic:
	''' + MAG + '''
	return -1;
	}
	''' + SZ + '''
	return -3;
}
'''),
        S(pin, 'nest3', '''	if (blsize <= size) {
	m = bl[0];
@P	if ((m & 0x43) == 0x43) {
	switch (type) {
''', '''	return 0;
bad:
	''' + BAD + '''
	return -2;
	} else {
	goto magic;
	}
	} else {
	''' + SZ + '''
	return -3;
	}
magic:
	''' + MAG + '''
	return -1;
}
'''),
        S(pin, 'ret_var', '''	if (blsize > size) {
		ret = -3;
		goto sizeerr;
	}
	m = bl[0];
@P	if ((m & 0x43) != 0x43)
		goto magic;
	switch (type) {
''', '''	return 0;
bad:
	''' + BAD + '''
	return -2;
sizeerr:
	''' + SZ + '''
	return ret;
magic:
	''' + MAG + '''
	return -1;
}
'''),
    ]
AXES = [shapes, [
    ('', []),
    ('d', [('uint32_t blsize, c;\n\tint m, dead;', 'uint32_t blsize, c;\n\tint m, dead, ret;')]),
]]
