"""checkBl with the range test before the switch and plain `if (c != crc) goto bad` arms, in place of crcSame and seven logs; which of no-early-inlining, hot label, blMagic, the two pins are still needed."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g114', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd114.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
SZ, CRC = g.SZ, g.CRC
MAGM = g.MAG0.replace('bl[0], bl[1]', 'm, bl[1]')


def PRE(t):
    return t


BM = 'static void blMagic(const uint8_t *bl, int *m)\n{\n\t*m = bl[0];\n}\n\n'


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    R = '\tif ((uint32_t)(type - 5) > 16) {\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n'
    for nei, hot, bm, pt, pm, six in itertools.product((1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1)):
        h, sw = g.switch('goto', 'goto magic')
        s = (BM if bm else '') + ('__attribute__((optimize("no-early-inlining")))\n' if nei else '')
        s += 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize, c;\n\tint m;\n\n'
        s += '\t__asm__("" : : "D"(type));\n' if pt else ''
        s += '\tblsize = getBeU32(bl + 12);\n\tif (blsize > size)\n\t\tgoto toobig;\n'
        s += '\tblMagic(bl, &m);\n' if bm else '\tm = bl[0];\n'
        s += '\t__asm__("" :: "a"(m));\n' if pm else ''
        s += '\tif ((m & 0x43) != 0x43)\n\t\tgoto magic;\n' + R + sw
        s += 'toobig: __attribute__((hot));\n' if hot else 'toobig:\n'
        s += '\t' + SZ + '\treturn -3;\nmagic:\n\t' + MAGM + '\treturn -1;\n}\n\n'
        t = base[:a] + s + base[b:]
        if six:
            t = t.replace('uint32_t r6 = checkBl(e->data, e->size, 6, e->crc);', 'uint32_t r6 = checkBl(e->data, e->size, type, e->crc);')
        out.append(('nei%d hot%d bm%d pt%d pm%d six%d' % (nei, hot, bm, pt, pm, six), t))
    return out
