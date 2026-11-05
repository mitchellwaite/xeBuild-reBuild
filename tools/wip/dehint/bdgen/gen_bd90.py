"""checkBl, whole-function forms with no hints: failure falls out of the switch to the crc log (`default: break`, c = 0 at the declaration, which is where
the reference's `xor eax,eax` before the log could come from), success returns from the arm."""
import itertools

CRCLOG = 'log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);\n'
SZLOG = 'log_printf(0, "\\n\\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\\n", blsize, size);\n'
MAGLOG = 'log_printf(0, "\\n\\n***** ERROR: BL magic check %c%c for type %d failed!\\n", bl[0], bl[1], type);\n'

ARMS = [
    ("5:\n\tcase 6:\n\tcase 11:\n\tcase 17", 'B', 0x10, 0x30, None),
    ("7:\n\tcase 18", 'D', 0x10, 0x10, None),
    ("8:\n\tcase 19", 'E', 0x10, 0x10, (2, 4)),
    ("9:\n\tcase 15:\n\tcase 20", 'F', 0x20, 0x210, (20, 22)),
    ("10:\n\tcase 16:\n\tcase 21", 'G', 0x10, 0x10, None),
    ("12", 'C', 0x10, 0x10, 'skip'),
    ("13", 'D', 0x10, 0x10, 'skip'),
]


def test(form, tail):
    """the crc test of an arm; tail runs on success, then the arm returns 0"""
    if form == 'eqret' and not tail:
        return '\t\tif (c == crc)\n\t\t\treturn 0;\n\t\tbreak;\n'
    if form == 'eqret2' and not tail:
        return '\t\tif (crc == c)\n\t\t\treturn 0;\n\t\tbreak;\n'
    if form == 'nested' or tail:
        if form in ('nebrk',) or tail and form != 'nested':
            return '\t\tif (c != crc)\n\t\t\tbreak;\n' + tail + '\t\treturn 0;\n'
        return '\t\tif (c == crc) {\n' + tail.replace('\t\t', '\t\t\t') + '\t\t\treturn 0;\n\t\t}\n\t\tbreak;\n'
    return '\t\tif (c != crc)\n\t\t\tbreak;\n\t\treturn 0;\n'


def body(form):
    s = '\tswitch (type) {\n'
    for lab, ch, off, n, x in ARMS:
        s += "\tcase %s:\n\t\tif (bl[1] != '%s')\n\t\t\tgoto magic;\n\t\tmemset(bl + 0x%x, 0, 0x%x);\n" % (lab, ch, off, n)
        if x == 'skip':
            s += '\t\tif (crc == 0xffffffff)\n\t\t\treturn 0;\n'
        s += '\t\tc = crc32(bl, blsize);\n'
        tail = ''
        if isinstance(x, tuple):
            tail = '\t\traiseKernel(getBeU16(bl), getBeU16(bl + %d), getBeU16(bl + %d));\n' % x
        s += test(form, tail)
    s += "\tcase 14:\n\t\tif (bl[1] != 'E')\n\t\t\tgoto magic;\n\t\tmemset(bl + 0x10, 0, 0x10);\n\t\tc = crc32(bl, blsize);\n"
    s += '\t\traiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));\n\t\tif (crc == 0xffffffff)\n\t\t\treturn 0;\n\t\tc = crc32(bl, blsize);\n'
    s += test(form, '')
    s += '\tdefault:\n\t\tbreak;\n\t}\n'
    return s


def fn(form, shape, mform):
    sw = body(form)
    h = 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize, c = 0;\n'
    if mform == 'm':
        h += '\tint m;\n'
        mt = '\tm = bl[0];\n\tif ((m & 0x43) != 0x43)\n\t\tgoto magic;\n'
        ml = MAGLOG.replace('bl[0], bl[1]', 'm, bl[1]')
    else:
        mt = '\tif ((bl[0] & 0x43) != 0x43)\n\t\tgoto magic;\n'
        ml = MAGLOG
    h += '\n\tblsize = getBeU32(bl + 12);\n'
    if shape == 'goto':
        return h + '\tif (blsize > size)\n\t\tgoto toobig;\n' + mt + sw + '\t' + CRCLOG + '\treturn -2;\ntoobig:\n\t' + SZLOG + '\treturn -3;\nmagic:\n\t' + ml + '\treturn -1;\n}\n\n'
    if shape == 'nest':
        ind = lambda x: ''.join('\t' + l + '\n' if l else '\n' for l in x.split('\n')[:-1])
        return h + '\tif (blsize <= size) {\n' + ind(mt) + ind(sw) + '\t\t' + CRCLOG + '\t\treturn -2;\n\t}\n\t' + SZLOG + '\treturn -3;\nmagic:\n\t' + ml + '\treturn -1;\n}\n\n'
    raise ValueError(shape)


def PRE(t):
    return t.replace('uint32_t r6 = checkBl(e->data, e->size, 6, e->crc);', 'uint32_t r6 = checkBl(e->data, e->size, type, e->crc);')


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    for form, shape, m in itertools.product(('eqret', 'eqret2', 'nested', 'nebrk'), ('goto', 'nest'), ('m', 'n')):
        out.append(('%s %s %s' % (form, shape, m), base[:a] + fn(form, shape, m) + base[b:]))
    return out
