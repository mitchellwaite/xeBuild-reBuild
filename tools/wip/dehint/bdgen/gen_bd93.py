"""checkBl, hint-free but for the m pin (kept as a marker for now): forms of the size failure, to get its frequency into [1000, 2000), crossed with forms of the crc arms."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g91', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd91.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
PRE = g.PRE
SZ = g.SZLOG
PIN = os.environ.get('PIN', '1') == '1'
HEAD = 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize, c;\n\tint m;\n'
TB = 'static int blTooBig(uint32_t blsize, uint32_t size)\n{\n\t' + SZ + '\treturn -3;\n}\n\n'
TB0 = 'static void blTooBig(uint32_t blsize, uint32_t size)\n{\n\t' + SZ + '}\n\n'
MT = '\tm = bl[0];\n' + ('\t__asm__("" :: "a"(m));\n' if PIN else '') + '\tif ((m & 0x43) != 0x43)\n\t\tgoto magic;\n'
MAG = 'magic:\n\t' + g.MAGLOG + '\treturn -1;\n}\n\n'
SIZE = {
    'goto': ('', '\tif (blsize > size)\n\t\tgoto toobig;\n', 'toobig:\n\t' + SZ + '\treturn -3;\n'),
    'helper': (TB, '\tif (blsize > size)\n\t\treturn blTooBig(blsize, size);\n', ''),
    'helperg': (TB, '\tif (blsize > size)\n\t\tgoto toobig;\n', 'toobig:\n\treturn blTooBig(blsize, size);\n'),
    'r': ('', '\tif (blsize > size)\n\t\tgoto toobig;\n', 'toobig:\n\t' + SZ + '\tr = -3;\n\treturn r;\n'),
    'var': ('', '\tr = -3;\n\tif (blsize > size)\n\t\tgoto toobig;\n', 'toobig:\n\t' + SZ + '\treturn r;\n'),
    'var2': ('', '\tif (blsize > size) {\n\t\tr = -3;\n\t\tgoto toobig;\n\t}\n', 'toobig:\n\t' + SZ + '\treturn r;\n'),
    'var3': ('', '\tr = blsize > size ? -3 : 0;\n\tif (r)\n\t\tgoto toobig;\n', 'toobig:\n\t' + SZ + '\treturn r;\n'),
    'var4': ('', '\tr = 0;\n\tif (blsize > size)\n\t\tr = -3;\n\tif (r)\n\t\tgoto toobig;\n', 'toobig:\n\t' + SZ + '\treturn r;\n'),
    'void': (TB0, '\tif (blsize > size) {\n\t\tblTooBig(blsize, size);\n\t\treturn -3;\n\t}\n', ''),
}


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    for form, (sz, (h0, test, tail)) in itertools.product(('goto', 'arm'), SIZE.items()):
        h, sw = g.switch(form)
        r = '\tint r;\n' if sz.startswith('var') or sz == 'r' else ''
        s = h + h0 + HEAD + r + '\n\tblsize = getBeU32(bl + 12);\n' + test + MT + sw + tail + MAG
        out.append(('%s %s' % (form, sz), base[:a] + s + base[b:]))
    return out
