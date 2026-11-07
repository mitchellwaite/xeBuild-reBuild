"""Attempt 52, diagnostic: the fuse helper made IPA-only by moving buildFlash's salt memset into it
(one call: growth x 2 > 14).  Not natural (a helper that clears the salt and returns the fuse flag);
run to see whether a call-holding helper with an early-return dev arm matches as a whole.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a52_devms.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
BASE = H.BASE
OLD = '''	memset(salt, 0, sizeof(salt));
	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		fuse = xb.glitch2mfg != 0;
		if (__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0))
			fuse = 1;
	}
'''
DEV = 'xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16'
ANCHOR = '/* no blmod.bin: the console\'s, if any */'
BODIES = {
 'dret': '\tint fuse;\n\n\tmemset(salt, 0, 16);\n\tif (xb.type == BUILD_JTAG)\n\t\treturn 1;\n\tfuse = xb.glitch2mfg != 0;\n\tif (%s)\n\t\treturn 1;\n\treturn fuse;\n' % DEV,
 'flag': '\tint fuse = 1;\n\n\tmemset(salt, 0, 16);\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (%s)\n\t\t\tfuse = 1;\n\t}\n\treturn fuse;\n' % DEV,
 'dret2': '\tint fuse = 1;\n\n\tmemset(salt, 0, 16);\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (%s)\n\t\t\treturn 1;\n\t}\n\treturn fuse;\n' % DEV,
}
V = {}
for b in BODIES:
    def f(t, b=b):
        if OLD not in t:
            raise ValueError('old')
        t = t.replace(OLD, '\tfuse = initFlash(salt);\n', 1)
        return t.replace(ANCHOR, 'static int initFlash(uint8_t *salt)\n{\n' + BODIES[b] + '}\n\n' + ANCHOR, 1)
    V[b] = f
