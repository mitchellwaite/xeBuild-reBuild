"""checkBl in one function with the range test: errors set r and leave through one exit that tests it, so no constant reaches the return at profile_estimate: PRED_CALL and PRED_GOTO alone
on the size error.  The test is threaded away later.  Size has to land in [1000, 2000)."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g114', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd114.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
PRE = g.PRE
SZ, MAG0, CRC = g.SZ, g.MAG0, g.CRC
MAGM = MAG0.replace('bl[0], bl[1]', 'm, bl[1]')


def CASES(base):
    a = base.index('/* Borderline, for review: an out parameter')
    b = base.index('int verifyBlSigs(void)')
    out = []
    R = '\tif ((uint32_t)(type - 5) > 16) {\n\t\tc = 0;\n\t\tgoto bad;\n\t}\n'
    TAILS = {
        't1': 'done:\n\tif (r)\n\t\treturn r;\n\treturn 0;\n',
        't2': 'done:\n\tif (r < 0)\n\t\treturn r;\n\treturn 0;\n',
        't3': 'done:\n\treturn r < 0 ? r : 0;\n',
    }
    SIZEF = {
        'all': ('\t' + SZ + '\tr = -3;\n\tgoto done;\n', '\t' + MAGM + '\tr = -1;\n', '\t' + CRC + '\tr = -2;\n\tgoto done;\n'),
        'size': ('\t' + SZ + '\tr = -3;\n\tgoto done;\n', '\t' + MAGM + '\treturn -1;\n', '\t' + CRC + '\treturn -2;\n'),
        'sizem': ('\t' + SZ + '\tr = -3;\n\tgoto done;\n', '\t' + MAGM + '\tr = -1;\n', '\t' + CRC + '\treturn -2;\n'),
    }
    for (tn, tl), (sn, (zs, mg, cr)), pin, ok in itertools.product(TAILS.items(), SIZEF.items(), (0, 1), ('ret', 'r')):
        h, sw = g.switch('goto', 'goto magic')
        i = sw.index('\treturn 0;\nbad:\n')
        body = sw[:i]
        mt = '\tm = bl[0];\n' + ('\t__asm__("" :: "a"(m));\n' if pin else '') + '\tif ((m & 0x43) != 0x43)\n\t\tgoto magic;\n'
        succ = '\treturn 0;\n' if ok == 'ret' else '\tr = 0;\n\tgoto done;\n'
        s = h + 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize, c;\n\tint m, r;\n\n\tblsize = getBeU32(bl + 12);\n\tif (blsize > size)\n\t\tgoto toobig;\n'
        tailfirst = mg.endswith('r = -1;\n')
        s += mt + R + body + succ + 'bad:\n' + cr + 'toobig:\n' + zs + 'magic:\n' + mg
        if tailfirst:
            s += tl
        else:
            # magic returns by itself, the exit goes before it
            s = s.replace('magic:\n' + mg, '')
            s = s.replace('toobig:\n' + zs, 'toobig:\n' + zs.replace('\tgoto done;\n', '') + tl + 'magic:\n' + mg)
        s += '}\n\n'
        out.append(('%s %s pin%d ok=%s' % (tn, sn, pin, ok), base[:a] + s + base[b:]))
    return out
