"""checkBl, gen_bd116 widened: every exit form; looking for size in [1000, 2000), magic under 2000, bad under 1000."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g114', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd114.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
PRE = g.PRE
SZ, MAG0, CRC = g.SZ, g.MAG0, g.CRC
MAGM = MAG0.replace('bl[0], bl[1]', 'm, bl[1]')
PIN = '\t__asm__("" :: "a"(m));\n'


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    R = '\tif ((uint32_t)(type - 5) > 16) {\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n'
    D = {
        't1': '\tif (r)\n\t\treturn r;\n\treturn 0;\n',
        't2': '\tif (r < 0)\n\t\treturn r;\n\treturn 0;\n',
        't3': '\treturn r < 0 ? r : 0;\n',
        't5': '\tif (!r)\n\t\treturn 0;\n\treturn r;\n',
        't6': '\tif (r >= 0)\n\t\treturn 0;\n\treturn r;\n',
    }
    E = {'ret': lambda c: '\treturn %d;\n' % c, 'done': lambda c: '\tr = %d;\n\tgoto done;\n' % c}
    for dn, cr, mg, ok, zs in itertools.product(D, E, E, E, ('done', 'ret2')):
        h, sw = g.switch('goto', 'goto magic')
        body = sw[:sw.index('\treturn 0;\nbad:\n')]
        mt = '\tm = bl[0];\n' + PIN + '\tif ((m & 0x43) != 0x43)\n\t\tgoto magic;\n'
        s = h + 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize, c;\n\tint m, r;\n\n\tblsize = getBeU32(bl + 12);\n\tif (blsize > size)\n\t\tgoto toobig;\n'
        s += mt + R + body + E[ok](0) + 'bad:\n\t' + CRC + E[cr](-2)
        s += 'toobig:\n\t' + SZ + ('\tr = -3;\n\tgoto done;\n')
        s += 'magic:\n\t' + MAGM + E[mg](-1) + 'done:\n' + D[dn] + '}\n\n'
        if zs == 'ret2':
            continue
        out.append(('%s crc=%s mag=%s ok=%s' % (dn, cr, mg, ok), base[:a] + s + base[b:]))
    return out
