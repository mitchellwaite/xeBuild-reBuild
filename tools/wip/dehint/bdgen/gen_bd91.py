"""checkBl with no hints at all: where the crc test lives (a helper with calls, not early inlined), and where the magic and type part lives (a static function).
Targets: size log in [1000, 2000), bad under 1000, magic under 2000; m in eax follows, maybe."""
import itertools

CRCLOG = 'log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);\n'
SZLOG = 'log_printf(0, "\\n\\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\\n", blsize, size);\n'
MAGLOG = 'log_printf(0, "\\n\\n***** ERROR: BL magic check %c%c for type %d failed!\\n", m, bl[1], type);\n'

ARMS = [
    ("5:\n\tcase 6:\n\tcase 11:\n\tcase 17", 'B', 0x10, 0x30, None),
    ("7:\n\tcase 18", 'D', 0x10, 0x10, None),
    ("8:\n\tcase 19", 'E', 0x10, 0x10, (2, 4)),
    ("9:\n\tcase 15:\n\tcase 20", 'F', 0x20, 0x210, (20, 22)),
    ("10:\n\tcase 16:\n\tcase 21", 'G', 0x10, 0x10, None),
    ("12", 'C', 0x10, 0x10, 'skip'),
    ("13", 'D', 0x10, 0x10, 'skip'),
]

HELPERS = {
    # returns 1 if good
    'ok': ('''static int blCrcOk(const uint8_t *bl, uint32_t blsize, uint32_t crc)
{
	uint32_t c = crc32(bl, blsize);

	if (c == crc)
		return 1;
	''' + CRCLOG + '''	return 0;
}

''', '\t\tif (!blCrcOk(bl, blsize, crc))\n\t\t\treturn -2;\n'),
    # returns the error
    'err': ('''static int blCrcCheck(const uint8_t *bl, uint32_t blsize, uint32_t crc)
{
	uint32_t c = crc32(bl, blsize);

	if (c != crc) {
		''' + CRCLOG + '''		return -2;
	}
	return 0;
}

''', '\t\tr = blCrcCheck(bl, blsize, crc);\n\t\tif (r)\n\t\t\treturn r;\n'),
    # logs only
    'log': ('''static int blCrcFail(uint32_t c, uint32_t crc)
{
	''' + CRCLOG + '''	return -2;
}

''', '\t\tc = crc32(bl, blsize);\n\t\tif (c != crc)\n\t\t\treturn blCrcFail(c, crc);\n'),
    'arm': ('', '\t\tc = crc32(bl, blsize);\n\t\tif (c != crc) {\n\t\t\t' + CRCLOG + '\t\t\treturn -2;\n\t\t}\n'),
    'goto': ('', '\t\tc = crc32(bl, blsize);\n\t\tif (c != crc)\n\t\t\tgoto bad;\n'),
}


def switch(form):
    h, t = HELPERS[form]
    s = '\tswitch (type) {\n'
    for lab, ch, off, n, x in ARMS:
        s += "\tcase %s:\n\t\tif (bl[1] != '%s')\n\t\t\tgoto magic;\n\t\tmemset(bl + 0x%x, 0, 0x%x);\n" % (lab, ch, off, n)
        if x == 'skip':
            s += '\t\tif (crc == 0xffffffff)\n\t\t\tbreak;\n'
        s += t
        if isinstance(x, tuple):
            s += '\t\traiseKernel(getBeU16(bl), getBeU16(bl + %d), getBeU16(bl + %d));\n' % x
        s += '\t\tbreak;\n'
    s += "\tcase 14:\n\t\tif (bl[1] != 'E')\n\t\t\tgoto magic;\n\t\tmemset(bl + 0x10, 0, 0x10);\n\t\tc = crc32(bl, blsize);\n"
    s += '\t\traiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));\n\t\tif (crc == 0xffffffff)\n\t\t\tbreak;\n\t\tc = crc32(bl, blsize);\n\t\tif (c != crc)\n\t\t\tgoto bad;\n\t\tbreak;\n'
    s += '\tdefault:\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n\treturn 0;\nbad:\n\t' + CRCLOG + '\treturn -2;\n'
    return h, s


def fn(form, split, size):
    h, sw = switch(form)
    r = '\tint r;\n' if form == 'err' else ''
    mt = '\tm = bl[0];\n\tif ((m & 0x43) != 0x43)\n\t\tgoto magic;\n'
    magic = 'magic:\n\t' + MAGLOG + '\treturn -1;\n}\n\n'
    tb = ''
    if size == 'helper':
        tb = 'static int blTooBig(uint32_t blsize, uint32_t size)\n{\n\t' + SZLOG + '\treturn -3;\n}\n\n'
    if split:
        inner = 'static int blCheckType(uint8_t *bl, uint32_t blsize, int type, uint32_t crc)\n{\n\tuint32_t c;\n\tint m;\n' + r + '\n' + mt + sw + magic
        out = h + inner + tb + 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize;\n'
        if size == 'first':
            out += '\n\tblsize = getBeU32(bl + 12);\n\tif (blsize > size) {\n\t\t' + SZLOG + '\t\treturn -3;\n\t}\n\treturn blCheckType(bl, blsize, type, crc);\n}\n\n'
        elif size == 'last':
            out += '\n\tblsize = getBeU32(bl + 12);\n\tif (blsize <= size)\n\t\treturn blCheckType(bl, blsize, type, crc);\n\t' + SZLOG + '\treturn -3;\n}\n\n'
        elif size == 'var':
            out += '\tint r;\n\n\tblsize = getBeU32(bl + 12);\n\tif (blsize <= size)\n\t\tr = blCheckType(bl, blsize, type, crc);\n\telse {\n\t\t' + SZLOG + '\t\tr = -3;\n\t}\n\treturn r;\n}\n\n'
        elif size == 'var2':
            out += '\tint r = -3;\n\n\tblsize = getBeU32(bl + 12);\n\tif (blsize > size)\n\t\t' + SZLOG + '\telse\n\t\tr = blCheckType(bl, blsize, type, crc);\n\treturn r;\n}\n\n'
        elif size == 'helper':
            out += '\n\tblsize = getBeU32(bl + 12);\n\tif (blsize > size)\n\t\treturn blTooBig(blsize, size);\n\treturn blCheckType(bl, blsize, type, crc);\n}\n\n'
        return out
    out = h + tb + 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize, c;\n\tint m;\n' + r + '\n\tblsize = getBeU32(bl + 12);\n'
    if size == 'helper':
        return out + '\tif (blsize > size)\n\t\treturn blTooBig(blsize, size);\n' + mt + sw + magic
    if size == 'first':
        return out + '\tif (blsize > size)\n\t\tgoto toobig;\n' + mt + sw + 'toobig:\n\t' + SZLOG + '\treturn -3;\n' + magic
    return None


def PRE(t):
    return t.replace('uint32_t r6 = checkBl(e->data, e->size, 6, e->crc);', 'uint32_t r6 = checkBl(e->data, e->size, type, e->crc);')


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    for form, split, size in itertools.product(HELPERS, (0, 1), ('first', 'last', 'var', 'var2', 'helper')):
        s = fn(form, split, size)
        if s:
            out.append(('%s split%d %s' % (form, split, size), base[:a] + s + base[b:]))
    return out
