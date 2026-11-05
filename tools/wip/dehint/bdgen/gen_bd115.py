"""checkBl in one function, range test before the switch: everything is right but the size error's frequency (880 with the hot label, it needs 1000).  Nesting in place of the goto (no goto
prediction), with the label or not, the m pin or not."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g114', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd114.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
PRE = g.PRE
SZ, MAG0 = g.SZ, g.MAG0
MAGM = MAG0.replace('bl[0], bl[1]', 'm, bl[1]')


def ind(x):
    return ''.join('\t' + l + '\n' if l else '\n' for l in x.split('\n')[:-1])


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    R = '\tif ((uint32_t)(type - 5) > 16) {\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n'
    for form, shape, hot, pin in itertools.product(('goto', 'arm'), ('goto', 'nest', 'nest2'), (0, 1), (0, 1)):
        h, sw = g.switch(form, 'goto magic')
        mt = '\tm = bl[0];\n' + ('\t__asm__("" :: "a"(m));\n' if pin else '') + '\tif ((m & 0x43) != 0x43)\n\t\tgoto magic;\n'
        head = h + 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize, c;\n\tint m;\n\n\tblsize = getBeU32(bl + 12);\n'
        hl = 'toobig: __attribute__((hot));\n' if hot else ''
        ml = 'magic:\n\t' + MAGM + '\treturn -1;\n}\n\n'
        if shape == 'goto':
            s = head + '\tif (blsize > size)\n\t\tgoto toobig;\n' + mt + R + sw + (hl or 'toobig:\n') + '\t' + SZ + '\treturn -3;\n' + ml
        elif shape == 'nest':
            s = head + '\tif (blsize <= size) {\n' + ind(mt + R + sw) + '\t}\n' + hl + '\t' + SZ + '\treturn -3;\n' + ml
        else:
            s = head + '\tif (blsize <= size) {\n' + ind(mt + R + sw) + '\t} else {\n' + ('\t' + hl if hl else '') + '\t\t' + SZ + '\t\treturn -3;\n\t}\n' + ml
        out.append(('%s %s hot%d pin%d' % (form, shape, hot, pin), base[:a] + s + base[b:]))
    return out
