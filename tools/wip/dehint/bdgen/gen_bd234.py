"""findSmcConfig (attempt 12): gen_bd233's `wh` loops (layout right with no expects) with neutral declaration and type
choices, to see whether any puts buf in edi and next in esi as the reference has them (the pin's job)."""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints, bdrun

LOOP = '''	while (i + N <= size && found != 1) {
		found = smcConfigOk(buf + i);
		if (found != 1)
			i += N;
	}
'''
ITYPE = ['uint32_t', 'unsigned', 'int', 'size_t']
BUF = ['uint8_t *buf', 'const uint8_t *buf']
DECL = ['if', 'fi', 'init', 'one']
RESET = ['in', 'out']  # i = 0 inside the !found block, or a second index j


def fn(it, bf, dc, rs):
    l1 = LOOP.replace('N', '0x200')
    if rs == 'in':
        l2 = '\t\ti = 0;\n' + ''.join('\t' + l for l in LOOP.replace('N', '0x210').splitlines(True))
        post = '\t}\n'
    else:
        l2 = '\t\ti = 0;\n' + ''.join('\t' + l for l in LOOP.replace('N', '0x210').splitlines(True))
        post = '\t}\n'
    if dc == 'if':
        d = '\t%s i = 0;\n\tint found = 0;\n' % it
    elif dc == 'fi':
        d = '\tint found = 0;\n\t%s i = 0;\n' % it
    elif dc == 'init':
        d = '\t%s i;\n\tint found;\n\n\ti = 0;\n\tfound = 0;\n' % it
    else:
        d = '\t%s i;\n\tint found;\n\n\tfound = 0;\n\ti = 0;\n' % it
    return ('static int findSmcConfig(%s, int size, uint32_t *pos)\n{\n' % bf + d + '\n' + l1 +
            '\tif (!found) {\n' + l2 + post + '\t*pos = i;\n\treturn found;\n}\n')


def CASES(base):
    t0 = bdhints.off(base, 'exp_200', 'exp_210', 'pin_i')
    i, j = bdrun.fnspan(t0, 'static int findSmcConfig(')
    out = []
    for it, bf, dc in itertools.product(ITYPE, BUF, DECL):
        out.append(('%s %s %s' % (it, bf.split()[0], dc), t0[:i] + fn(it, bf, dc, 'in') + t0[j:]))
    return out


FOCUS = ['_extractSmcConfig']
