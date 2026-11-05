"""As gen_bd100, with the m test inside the static function too: a call right after the size test, on the normal edge."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g91', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd91.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
PRE = g.PRE
SZ = g.SZLOG
MAG0 = g.MAGLOG.replace('m, bl[1]', 'bl[0], bl[1]')
HEAD = 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize;\n\tint r;\n'


def inner(form, code, pin):
    h, sw = g.switch(form)
    sw = sw.replace('goto magic;', 'return %s;' % code)
    return h + 'static int blCheckType(uint8_t *bl, uint32_t blsize, int type, uint32_t crc)\n{\n\tuint32_t c;\n\n\tif ((bl[0] & 0x43) != 0x43)\n\t\treturn %s;\n' % code + sw + '}\n\n'


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    TESTS = {
        'ne-1': ('-1', '\tr = blCheckType(bl, blsize, type, crc);\n\tif (r != -1)\n\t\treturn r;\n\tgoto magic;\n'),
        'eq1': ('1', '\tr = blCheckType(bl, blsize, type, crc);\n\tif (r == 1)\n\t\tgoto magic;\n\treturn r;\n'),
        'nest': ('-1', '\tr = blCheckType(bl, blsize, type, crc);\n\tif (r == -1) {\nmagic:\n\t\t' + MAG0 + '\t}\n\treturn r;\n'),
    }
    for form, (tn, (code, t)), hot in itertools.product(('goto', 'arm'), TESTS.items(), (0, 1)):
        lab = 'toobig: __attribute__((hot));\n' if hot else 'toobig:\n'
        s = inner(form, code, 0) + HEAD + '\n\tblsize = getBeU32(bl + 12);\n\tif (blsize > size)\n\t\tgoto toobig;\n'
        s += t + lab + '\t' + SZ + '\treturn -3;\nmagic:\n\t' + MAG0 + '\treturn -1;\n}\n\n'
        if tn == 'nest':
            s = s.replace('magic:\n\t\t', '\t\t').replace('}\n\treturn r;\ntoobig', '}\n\treturn r;\ntoobig').replace('magic:\n\t' + MAG0 + '\treturn -1;\n', '')
        out.append(('%s %s hot%d' % (form, tn, hot), base[:a] + s + base[b:]))
    return out
