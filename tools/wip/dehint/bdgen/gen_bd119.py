"""checkBl from gen_bd118's nei1 hot1 bm1 pt1 pm1 (0 loose, 7 strict): the default block is aligned because its frequency is 122, over the 1% threshold.  Forms of the range test, and of what's upstream, to get it under 100."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g114', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd114.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
SZ, CRC = g.SZ, g.CRC
MAGM = g.MAG0.replace('bl[0], bl[1]', 'm, bl[1]')
BM = 'static void blMagic(const uint8_t *bl, int *m)\n{\n\t*m = bl[0];\n}\n\n'


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    RF = {
        'u': '\tif ((uint32_t)(type - 5) > 16) {\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n',
        'u2': '\tif ((uint32_t)type - 5 > 16) {\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n',
        'ge': '\tif ((uint32_t)(type - 5) >= 17) {\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n',
        'c0': '\tc = 0;\n\tif ((uint32_t)(type - 5) > 16)\n\t\tgoto bad;\n',
        'or': '\tif (type < 5 || type > 21) {\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n',
        'two': '\tif (type < 5) {\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n\tif (type > 21) {\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n',
        'c0or': '\tc = 0;\n\tif (type < 5 || type > 21)\n\t\tgoto bad;\n',
        'ret': '\tif ((uint32_t)(type - 5) > 16) {\n\t\tc = 0;\n\t\tgoto bad;\n\t} else\n',
    }
    MF = {
        'ne': '\tif ((m & 0x43) != 0x43)\n\t\tgoto magic;\n',
        'not': '\tif (!((m & 0x43) == 0x43))\n\t\tgoto magic;\n',
        'xor': '\tif ((m & 0x43) - 0x43)\n\t\tgoto magic;\n',
        'nx': '\tif (~m & 0x43)\n\t\tgoto magic;\n',
    }
    for (rn, rf), (mn, mf), pos in itertools.product(RF.items(), MF.items(), ('after', 'before')):
        h, sw = g.switch('goto', 'goto magic')
        s = BM + '__attribute__((optimize("no-early-inlining")))\nint checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize, c;\n\tint m;\n\n\t__asm__("" : : "D"(type));\n'
        s += '\tblsize = getBeU32(bl + 12);\n\tif (blsize > size)\n\t\tgoto toobig;\n\tblMagic(bl, &m);\n\t__asm__("" :: "a"(m));\n'
        s += (mf + rf) if pos == 'after' else (rf + mf)
        s += sw + 'toobig: __attribute__((hot));\n\t' + SZ + '\treturn -3;\nmagic:\n\t' + MAGM + '\treturn -1;\n}\n\n'
        out.append(('%s %s %s' % (rn, mn, pos), base[:a] + s + base[b:]))
    return out
