"""checkBl: the switch as a static function with calls in it (not early inlined), the caller logging a magic failure the helper reports, which keeps the text order crc, size, magic."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g91', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd91.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
PRE = g.PRE
SZ = g.SZLOG
MAGLOG = g.MAGLOG
PIN = os.environ.get('PIN', '1') == '1'
HEAD = 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize;\n\tint m, r;\n'
MT = '\tm = bl[0];\n' + ('\t__asm__("" :: "a"(m));\n' if PIN else '') + '\tif ((m & 0x43) != 0x43)\n\t\tgoto magic;\n'


def inner(form, code):
    h, sw = g.switch(form)
    sw = sw.replace('goto magic;', 'return %s;' % code)
    return h + 'static int blCheckType(uint8_t *bl, uint32_t blsize, int type, uint32_t crc)\n{\n\tuint32_t c;\n\n' + sw + '}\n\n'


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    TESTS = {
        'ne-1': ('-1', '\tr = blCheckType(bl, blsize, type, crc);\n\tif (r != -1)\n\t\treturn r;\n\tgoto magic;\n'),
        'eq-1': ('-1', '\tr = blCheckType(bl, blsize, type, crc);\n\tif (r == -1)\n\t\tgoto magic;\n\treturn r;\n'),
        'eq1': ('1', '\tr = blCheckType(bl, blsize, type, crc);\n\tif (r == 1)\n\t\tgoto magic;\n\treturn r;\n'),
        'ne1': ('1', '\tr = blCheckType(bl, blsize, type, crc);\n\tif (r != 1)\n\t\treturn r;\n\tgoto magic;\n'),
        'lt-2': ('-1', '\tr = blCheckType(bl, blsize, type, crc);\n\tif (r >= -1 && r)\n\t\tgoto magic;\n\treturn r;\n'),
    }
    for form, (tn, (code, t)), hot, sw in itertools.product(('goto', 'arm'), TESTS.items(), (0, 1), (0, 1)):
        lab = 'toobig: __attribute__((hot));\n' if hot else 'toobig:\n'
        s = inner(form, code) + HEAD + '\n\tblsize = getBeU32(bl + 12);\n\tif (blsize > size)\n\t\tgoto toobig;\n'
        s += MT + t + lab + '\t' + SZ + '\treturn -3;\nmagic:\n\t' + MAGLOG.replace('m, bl[1]', 'm, bl[1]') + '\treturn -1;\n}\n\n'
        if sw:
            continue
        out.append(('%s %s hot%d' % (form, tn, hot), base[:a] + s + base[b:]))
    return out
