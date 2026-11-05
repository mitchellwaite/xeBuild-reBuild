"""checkBl without no-early-inlining, crcSame, blMagic, the type pin: hot label kept, crc arms forms, the m pin kept; how much is left?  Also a helper with calls on the normal edge."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g91', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd91.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
PRE = g.PRE
SZ = g.SZLOG
HEAD = 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize, c;\n\tint m;\n'
MAG = 'magic:\n\t' + g.MAGLOG + '\treturn -1;\n}\n\n'


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    for form, pin, pt, hot in itertools.product(('goto', 'arm'), (0, 1), (0, 1), (0, 1, 2)):
        h, sw = g.switch(form)
        mt = '\tm = bl[0];\n' + ('\t__asm__("" :: "a"(m));\n' if pin else '') + '\tif ((m & 0x43) != 0x43)\n\t\tgoto magic;\n'
        lab = 'toobig: __attribute__((hot));\n' if hot == 1 else 'toobig:\n'
        test = '\tif (blsize > size)\n\t\tgoto toobig;\n'
        if hot == 2:
            test = '\tif (__builtin_expect(blsize > size, 1))\n\t\tgoto toobig;\n'
        s = h + HEAD + '\n' + ('\t__asm__("" : : "D"(type));\n' if pt else '') + '\tblsize = getBeU32(bl + 12);\n' + test + mt + sw + lab + '\t' + SZ + '\treturn -3;\n' + MAG
        out.append(('%s pin%d pt%d hot%d' % (form, pin, pt, hot), base[:a] + s + base[b:]))
    return out
