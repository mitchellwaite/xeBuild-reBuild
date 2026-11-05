"""checkBl hint-free: the size failure's log and its return in two steps, so the log isn't under the negative return's prediction at profile_estimate; a jump thread joins them afterwards."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g91', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd91.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
PRE = g.PRE
SZ = g.SZLOG
PIN = os.environ.get('PIN', '1') == '1'
HEAD = 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize, c;\n\tint m;\n'
MT = '\tm = bl[0];\n' + ('\t__asm__("" :: "a"(m));\n' if PIN else '') + '\tif ((m & 0x43) != 0x43)\n\t\tgoto magic;\n'
MAG = 'magic:\n\t' + g.MAGLOG + '\treturn -1;\n}\n\n'
OK = 'static int blSizeOk(uint32_t blsize, uint32_t size)\n{\n\tif (blsize > size) {\n\t\t' + SZ + '\t\treturn 0;\n\t}\n\treturn 1;\n}\n\n'
OK2 = 'static int blSizeOk(uint32_t blsize, uint32_t size)\n{\n\tif (blsize <= size)\n\t\treturn 1;\n\t' + SZ + '\treturn 0;\n}\n\n'
BAD = 'static int blTooBig(uint32_t blsize, uint32_t size)\n{\n\tif (blsize > size) {\n\t\t' + SZ + '\t\treturn 1;\n\t}\n\treturn 0;\n}\n\n'
SIZE = {
    'ok': (OK, '\tif (!blSizeOk(blsize, size))\n\t\treturn -3;\n', ''),
    'ok2': (OK2, '\tif (!blSizeOk(blsize, size))\n\t\treturn -3;\n', ''),
    'bad': (BAD, '\tif (blTooBig(blsize, size))\n\t\treturn -3;\n', ''),
    'okg': (OK, '\tif (!blSizeOk(blsize, size))\n\t\tgoto toobig;\n', 'toobig:\n\treturn -3;\n'),
    'flag': ('', '\ttoobig = blsize > size;\n\tif (toobig)\n\t\t' + SZ + '\tif (toobig)\n\t\treturn -3;\n', ''),
    'flag2': ('', '\ttoobig = 0;\n\tif (blsize > size) {\n\t\t' + SZ + '\t\ttoobig = 1;\n\t}\n\tif (toobig)\n\t\treturn -3;\n', ''),
    'r': ('', '\tr = 0;\n\tif (blsize > size) {\n\t\t' + SZ + '\t\tr = -3;\n\t}\n\tif (r)\n\t\treturn r;\n', ''),
    'r2': ('', '\tr = 0;\n\tif (blsize > size) {\n\t\t' + SZ + '\t\tr = -3;\n\t}\n\tif (r < 0)\n\t\treturn r;\n', ''),
    'r3': ('', '\tr = 0;\n\tif (blsize > size) {\n\t\t' + SZ + '\t\tr = -3;\n\t}\n\tif (!r) {\n\t\t' + '@BODY@' + '\t}\n\treturn r;\n', ''),
}


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    for form, (sz, (h0, test, tail)) in itertools.product(('goto', 'arm'), SIZE.items()):
        if '@BODY@' in test:
            continue
        h, sw = g.switch(form)
        r = ''
        if sz.startswith('flag'):
            r = '\tint toobig;\n'
        if sz.startswith('r'):
            r = '\tint r;\n'
        s = h + h0 + HEAD + r + '\n\tblsize = getBeU32(bl + 12);\n' + test + MT + sw + tail + MAG
        out.append(('%s %s' % (form, sz), base[:a] + s + base[b:]))
    return out
