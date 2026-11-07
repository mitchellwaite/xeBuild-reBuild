"""Attempt 52: exp_devgl through a shared "virtual fuses in use" predicate (glitch2mfg or a devgl
type), the test addBlsToImage (case 23's 0x60 and case 24), addUpdateBls (case 24) and buildFlash
all make.  Bodies x where it is used x the expect kept ('E') or off ('n').
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a52_dev.py"""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
BASE = H.BASE
ANCHOR = '/* write the flash files\' bootloaders into the image.'
DEV = 'xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16'
BODIES = {
    'or': '\treturn xb.glitch2mfg || %s;\n' % DEV,
    'orne': '\treturn xb.glitch2mfg != 0 || %s;\n' % DEV,
    'flag': '\tint fuse = xb.glitch2mfg != 0;\n\n\tif (%s)\n\t\tfuse = 1;\n\treturn fuse;\n' % DEV,
    'g1st': '\tif (xb.glitch2mfg)\n\t\treturn 1;\n\treturn %s;\n' % DEV,
    'd1st': '\tif (%s)\n\t\treturn 1;\n\treturn xb.glitch2mfg != 0;\n' % DEV,
    'dret': '\tint fuse = xb.glitch2mfg != 0;\n\n\tif (%s)\n\t\treturn 1;\n\treturn fuse;\n' % DEV,
}
FN = '/* glitch2 mfg and devgl images carry virtual fuses (type 24) */\nstatic int vfusesUsed(void)\n{\n%s}\n\n'
BF_OLD = '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		fuse = xb.glitch2mfg != 0;
		if (__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0))
			fuse = 1;
	}
'''
BF = {
    'if': '\tfuse = 1;\n\tif (xb.type != BUILD_JTAG)\n\t\tfuse = vfusesUsed();\n',
    'or': '\tfuse = xb.type == BUILD_JTAG || vfusesUsed();\n',
}
C23_OLD = '''			if (xb.glitch2mfg)
				off += 0x60;
			else if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
				off += 0x60;
			else
				off += 0x10;
'''
C23 = '''			if (vfusesUsed())
				off += 0x60;
			else
				off += 0x10;
'''
C24_OLD = '			if (xb.glitch2mfg || xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) {\n'
C24 = '			if (vfusesUsed()) {\n'
WHERE = {'bf': (1, 0, 0), 'bf24': (1, 0, 2), 'bf23': (1, 1, 0), 'all': (1, 1, 2), 'not_bf': (0, 1, 2)}


def mk(b, bf, w, exp):
    def f(t):
        if not exp:
            t = t.replace(H.DEV[0], H.DEV[1], 1)
        a, c23, c24 = WHERE[w]
        if a:
            old = BF_OLD if exp else BF_OLD.replace('__builtin_expect(%s, 0)' % DEV, DEV)
            if old not in t:
                raise ValueError('bf')
            t = t.replace(old, BF[bf], 1)
        if c23:
            t = t.replace(C23_OLD, C23, 1)
        for _ in range(c24):
            if C24_OLD not in t:
                raise ValueError('c24')
            t = t.replace(C24_OLD, C24, 1)
        return t.replace(ANCHOR, FN % BODIES[b] + ANCHOR, 1)
    return f


V = {}
for b, bf, w, exp in itertools.product(BODIES, BF, WHERE, (0, 1)):
    if w == 'not_bf' and (bf != 'if' or not exp):
        continue
    if exp and w != 'not_bf':
        continue
    V['%s_%s_%s_%s' % (b, bf, w, 'E' if exp else 'n')] = mk(b, bf, w, exp)
