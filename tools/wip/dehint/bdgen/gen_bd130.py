"""checkBl with one error code: the arms only set r, one block at the end logs by r and returns it.  The text order crc, size, magic is then just the
order of the tests there, and the frequencies come from jump threading, not from the arms.  No attribute, no helper, no label, no pins."""
import itertools

CRCLOG = 'log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);\n'
SZLOG = 'log_printf(0, "\\n\\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\\n", blsize, size);\n'
MAGLOG = 'log_printf(0, "\\n\\n***** ERROR: BL magic check %c%c for type %d failed!\\n", m, bl[1], type);\n'

ARMS = [
    ([5, 6, 11, 17], 'B', 'bl + 0x10, 0, 0x30', None, 0),
    ([7, 18], 'D', 'bl + 0x10, 0, 0x10', None, 0),
    ([8, 19], 'E', 'bl + 0x10, 0, 0x10', 'raiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));', 0),
    ([9, 15, 20], 'F', 'bl + 0x20, 0, 0x210', 'raiseKernel(getBeU16(bl), getBeU16(bl + 20), getBeU16(bl + 22));', 0),
    ([10, 16, 21], 'G', 'bl + 0x10, 0, 0x10', None, 0),
    ([12], 'C', 'bl + 0x10, 0, 0x10', None, 1),
    ([13], 'D', 'bl + 0x10, 0, 0x10', None, 1),
    ([14], 'E', 'bl + 0x10, 0, 0x10', None, 2),
]


def arm(cases, ch, ms, after, kind, form):
    s = ''.join('\tcase %d:\n' % c for c in cases)
    if form == 'break':
        s += "\t\tif (bl[1] != '%s') {\n\t\t\tr = -1;\n\t\t\tbreak;\n\t\t}\n" % ch
        s += '\t\tmemset(%s);\n' % ms
        if kind == 2:
            s += '\t\tc = crc32(bl, blsize);\n\t\traiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));\n'
        if kind:
            s += '\t\tif (crc == 0xffffffff)\n\t\t\tbreak;\n'
        s += '\t\tc = crc32(bl, blsize);\n'
        if after:
            s += '\t\tif (c != crc) {\n\t\t\tr = -2;\n\t\t\tbreak;\n\t\t}\n\t\t%s\n' % after
        else:
            s += '\t\tif (c != crc)\n\t\t\tr = -2;\n'
        s += '\t\tbreak;\n'
    else:
        s += "\t\tif (bl[1] != '%s')\n\t\t\tr = -1;\n\t\telse {\n" % ch
        s += '\t\t\tmemset(%s);\n' % ms
        if kind == 2:
            s += '\t\t\tc = crc32(bl, blsize);\n\t\t\traiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));\n'
        if kind:
            s += '\t\t\tif (crc != 0xffffffff) {\n\t\t\t\tc = crc32(bl, blsize);\n\t\t\t\tif (c != crc)\n\t\t\t\t\tr = -2;\n\t\t\t}\n'
        else:
            s += '\t\t\tc = crc32(bl, blsize);\n\t\t\tif (c != crc)\n\t\t\t\tr = -2;\n'
            if after:
                s += '\t\t\telse\n\t\t\t\t%s\n' % after
        s += '\t\t}\n\t\tbreak;\n'
    return s


def switch(form, dflt):
    s = '\tswitch (type) {\n' + ''.join(arm(*a, form) for a in ARMS)
    if dflt == 'c0':
        s += '\tdefault:\n\t\tc = 0;\n\t\tr = -2;\n\t\tbreak;\n'
    else:
        s += '\tdefault:\n\t\tr = -2;\n\t\tbreak;\n'
    return s + '\t}\n'


def ind(x, n=1):
    return ''.join('\t' * n + l + '\n' if l else '\n' for l in x.split('\n')[:-1])


TAILS = {
    'chain': '\tif (r == -2)\n\t\t' + CRCLOG + '\telse if (r == -3)\n\t\t' + SZLOG + '\telse if (r == -1)\n\t\t' + MAGLOG,
    'seq': '\tif (r == -2)\n\t\t' + CRCLOG + '\tif (r == -3)\n\t\t' + SZLOG + '\tif (r == -1)\n\t\t' + MAGLOG,
    'sw': '\tswitch (r) {\n\tcase -2:\n\t\t' + CRCLOG + '\t\tbreak;\n\tcase -3:\n\t\t' + SZLOG + '\t\tbreak;\n\tcase -1:\n\t\t' + MAGLOG + '\t\tbreak;\n\t}\n',
    'nest': '\tif (r) {\n\t\tif (r == -2)\n\t\t\t' + CRCLOG + '\t\telse if (r == -3)\n\t\t\t' + SZLOG + '\t\telse\n\t\t\t' + MAGLOG + '\t}\n',
}


def PRE(b):
    return b.replace('uint32_t r6 = checkBl(e->data, e->size, 6, e->crc);', 'uint32_t r6 = checkBl(e->data, e->size, type, e->crc);')


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    for form, dflt, tail, head, ini in itertools.product(('break', 'else'), ('c0', 'init'), TAILS, ('else', 'goto', 'elseif'), ('decl', 'stmt')):
        sw = switch(form, dflt)
        decl = '\tuint32_t blsize, c%s;\n\tint m, r%s;\n\n' % (' = 0' if dflt == 'init' else '', ' = 0' if ini == 'decl' else '')
        s = 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n' + decl
        if ini == 'stmt':
            s += '\tr = 0;\n'
        s += '\tblsize = getBeU32(bl + 12);\n'
        mt = '\tm = bl[0];\n'
        if head == 'else':
            s += '\tif (blsize > size)\n\t\tr = -3;\n\telse {\n' + ind(mt + '\tif ((m & 0x43) != 0x43)\n\t\tr = -1;\n\telse {\n' + ind(sw) + '\t}\n') + '\t}\n'
        elif head == 'goto':
            s += '\tif (blsize > size) {\n\t\tr = -3;\n\t\tgoto done;\n\t}\n' + mt + '\tif ((m & 0x43) != 0x43) {\n\t\tr = -1;\n\t\tgoto done;\n\t}\n' + sw + 'done:\n'
        else:
            s += mt + '\tif (blsize > size)\n\t\tr = -3;\n\telse if ((m & 0x43) != 0x43)\n\t\tr = -1;\n\telse {\n' + ind(sw) + '\t}\n'
        s += TAILS[tail] + '\treturn r;\n}\n\n'
        out.append(('%s %s %s %s %s' % (form, dflt, tail, head, ini), base[:a] + s + base[b:]))
    return out
