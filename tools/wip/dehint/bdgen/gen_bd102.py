"""gen_bd101's best with its frequencies trimmed: bad 1089 -> under 1000, magic 2135 -> under 2000, size 1910 stays.  goto in the helper for magic failures, separate
identical cases to thin default's share of the switch, the type 14 crc failure's own log."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g91', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd91.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
PRE = g.PRE
SZ = g.SZLOG
CRC = g.CRCLOG
MAG0 = g.MAGLOG.replace('m, bl[1]', 'bl[0], bl[1]')
HEAD = 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize;\n\tint r;\n'


def arm(lab, ch, off, n, x, fail, crc14=None):
    s = "\tcase %s:\n\t\tif (bl[1] != '%s')\n\t\t\t%s;\n\t\tmemset(bl + 0x%x, 0, 0x%x);\n" % (lab, ch, fail, off, n)
    if x == 'skip':
        s += '\t\tif (crc == 0xffffffff)\n\t\t\tbreak;\n'
    s += '\t\tc = crc32(bl, blsize);\n\t\tif (c != crc) {\n\t\t\t' + CRC + '\t\t\treturn -2;\n\t\t}\n'
    if isinstance(x, tuple):
        s += '\t\traiseKernel(getBeU16(bl), getBeU16(bl + %d), getBeU16(bl + %d));\n' % x
    return s + '\t\tbreak;\n'


def inner(fail, split, c14, mtest):
    ARMS = [
        ("5:\n\tcase 6:\n\tcase 11:\n\tcase 17", 'B', 0x10, 0x30, None),
        ("7:\n\tcase 18", 'D', 0x10, 0x10, None),
        ("8:\n\tcase 19", 'E', 0x10, 0x10, (2, 4)),
        ("9:\n\tcase 15:\n\tcase 20", 'F', 0x20, 0x210, (20, 22)),
        ("10:\n\tcase 16:\n\tcase 21", 'G', 0x10, 0x10, None),
        ("12", 'C', 0x10, 0x10, 'skip'),
        ("13", 'D', 0x10, 0x10, 'skip'),
    ]
    if split == 1:
        ARMS[0] = ("5:\n\tcase 11:\n\tcase 17", 'B', 0x10, 0x30, None)
        ARMS.insert(1, ("6", 'B', 0x10, 0x30, None))
    if split == 2:
        ARMS[0] = ("5:\n\tcase 11:\n\tcase 17", 'B', 0x10, 0x30, None)
        ARMS.insert(1, ("6", 'B', 0x10, 0x30, None))
        ARMS[2] = ("7", 'D', 0x10, 0x10, None)
        ARMS.insert(3, ("18", 'D', 0x10, 0x10, None))
    sw = '\tswitch (type) {\n' + ''.join(arm(*a, fail) for a in ARMS)
    sw += "\tcase 14:\n\t\tif (bl[1] != 'E')\n\t\t\t%s;\n\t\tmemset(bl + 0x10, 0, 0x10);\n\t\tc = crc32(bl, blsize);\n" % fail
    sw += '\t\traiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));\n\t\tif (crc == 0xffffffff)\n\t\t\tbreak;\n\t\tc = crc32(bl, blsize);\n'
    if c14 == 'goto':
        sw += '\t\tif (c != crc)\n\t\t\tgoto bad;\n\t\tbreak;\n\tdefault:\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n\treturn 0;\nbad:\n\t' + CRC + '\treturn -2;\n'
    else:
        sw += '\t\tif (c != crc) {\nbad:\n\t\t\t' + CRC + '\t\t\treturn -2;\n\t\t}\n\t\tbreak;\n\tdefault:\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n\treturn 0;\n'
    tail = 'badmagic:\n\treturn -1;\n' if 'goto' in fail or mtest == 'goto' else ''
    mt = '\tif ((bl[0] & 0x43) != 0x43)\n\t\t%s;\n' % ('goto badmagic' if mtest == 'goto' else 'return -1')
    if mtest == 'nest':
        mt = '\tif ((bl[0] & 0x43) == 0x43)\n\t\t@@\n'
    return 'static int blCheckType(uint8_t *bl, uint32_t blsize, int type, uint32_t crc)\n{\n\tuint32_t c;\n\n' + mt + sw + tail + '}\n\n'


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    for fail, split, c14, mtest, hot in itertools.product(('return -1', 'goto badmagic'), (0, 1, 2), ('goto', 'label'), ('return', 'goto'), (1, 0)):
        lab = 'toobig: __attribute__((hot));\n' if hot else 'toobig:\n'
        s = inner(fail, split, c14, mtest) + HEAD + '\n\tblsize = getBeU32(bl + 12);\n\tif (blsize > size)\n\t\tgoto toobig;\n'
        s += '\tr = blCheckType(bl, blsize, type, crc);\n\tif (r != -1)\n\t\treturn r;\n\tgoto magic;\n' + lab + '\t' + SZ + '\treturn -3;\nmagic:\n\t' + MAG0 + '\treturn -1;\n}\n\n'
        out.append(('%s split%d c14=%s m=%s hot%d' % (fail, split, c14, mtest, hot), base[:a] + s + base[b:]))
    return out
