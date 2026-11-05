"""checkBl: the out-of-range type tested before the switch, so default's even share of the switch edges goes away (VRP then removes the switch's own bound test, the same one test).
Static function or not, with and without the hot label, forms of the range test and of its failure."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g91', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd91.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
PRE = g.PRE
SZ = g.SZLOG
CRC = g.CRCLOG
MAG0 = g.MAGLOG.replace('m, bl[1]', 'bl[0], bl[1]')


def switch(form, fail):
    h, s = g.switch(form)
    s = s.replace('goto magic;', fail + ';')
    # no default: types are in range here
    s = s.replace('\tdefault:\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n', '\t}\n')
    return h, s


RANGE = {
    'or': '\tif (type < 5 || type > 21) {\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n',
    'u': '\tif ((uint32_t)(type - 5) > 16) {\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n',
    'and': '\tc = 0;\n\tif (type >= 5 && type <= 21) {\n\t\t@@\n\t}\n',
}


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    for form, split, rn, hot in itertools.product(('goto', 'arm'), (0, 1), ('or', 'u'), (0, 1)):
        lab = 'toobig: __attribute__((hot));\n' if hot else 'toobig:\n'
        R = RANGE[rn]
        if split:
            h, sw = switch(form, 'return -1')
            inner = h + 'static int blCheckType(uint8_t *bl, uint32_t blsize, int type, uint32_t crc)\n{\n\tuint32_t c;\n\n\tif ((bl[0] & 0x43) != 0x43)\n\t\treturn -1;\n' + R + sw + '}\n\n'
            s = inner + 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize;\n\tint r;\n\n\tblsize = getBeU32(bl + 12);\n\tif (blsize > size)\n\t\tgoto toobig;\n'
            s += '\tr = blCheckType(bl, blsize, type, crc);\n\tif (r != -1)\n\t\treturn r;\n\tgoto magic;\n' + lab + '\t' + SZ + '\treturn -3;\nmagic:\n\t' + MAG0 + '\treturn -1;\n}\n\n'
        else:
            h, sw = switch(form, 'goto magic')
            s = h + 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize, c;\n\n\tblsize = getBeU32(bl + 12);\n\tif (blsize > size)\n\t\tgoto toobig;\n\tif ((bl[0] & 0x43) != 0x43)\n\t\tgoto magic;\n' + R + sw + lab + '\t' + SZ + '\treturn -3;\nmagic:\n\t' + MAG0 + '\treturn -1;\n}\n\n'
        out.append(('%s split%d %s hot%d' % (form, split, rn, hot), base[:a] + s + base[b:]))
    return out
